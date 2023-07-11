import os
import random

from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from fastapi.testclient import TestClient
from web3 import Account, Web3

from app import app
from app.core.models.score_submission import ScoreSubmission
from app.settings import settings
from app.util import get_timestamp
from . import *  # noqa

test_game_account: LocalAccount = Account.create(12)

print(f'Test game account: {test_game_account}')

os.environ['GAME_ADDRESS'] = test_game_account.address

settings.GAME_ADDRESS = test_game_account.address

client = TestClient(app)


def _sign(score: int, user: str, character_name: str, skin_id: str = 'base'):
    msg_hash = Web3.solidity_keccak(['address', 'string', 'string', 'uint256'],
                                    [user, character_name, skin_id, score])
    return Web3.to_hex(test_game_account.sign_message(encode_defunct(msg_hash)).signature)


def test_successful_score_sub(test_db):
    # prepare test data

    char1a = 1
    char1_name = 'Meowton'
    char1b = 2
    char2_name = 'Bistury'
    user1 = '0x3fB9A0A657858E66553D7BDa08368e7609E32C41'
    score1a = 10
    score1b = 15
    score1c = 20

    char2 = 2
    user2 = '0xdb857De484CF422748794b4a647dE0BBaA456Fa8'
    score2 = 18

    char3 = 1
    char3_name = 'Hammer'
    user3 = '0xB71F00C752fd6a97832e4cef14C31cc03802CB1D'
    score3 = 30

    # check that there is no data yet

    highscore = client.get(f'/api/v1/highscore', params={"user": user1, "character": char1a})
    assert highscore.status_code == 200
    assert highscore.json() is None

    # save submissions (three for user 1)

    # submission for user1 with score 1a and character 1a

    ticket1a = client.get('/api/v1/ticket').json()

    game = client.get(f'/api/v1/ticket/{ticket1a}')
    assert game.status_code == 200

    signature = _sign(score1a, user1, char1_name)

    score_sub1a = ScoreSubmission(
        ticket=ticket1a,
        user=user1,
        score=score1a,
        character_id=char1a,
        character_name=char1_name,
        end_timestamp=get_timestamp(),
        game_version='1.0.0',
        signature=signature,
    )

    res = client.post('/api/v1/score', json=score_sub1a.dict())
    assert res.status_code == 200

    # submission for user1 with score 1b and character 1a

    ticket1b = client.get('/api/v1/ticket').json()

    game = client.get(f'/api/v1/ticket/{ticket1b}')
    assert game.status_code == 200

    signature = _sign(score1b, user1, char1_name)

    score_sub1b = ScoreSubmission(
        ticket=ticket1b,
        user=user1,
        score=score1b,
        character_id=char1a,
        character_name=char1_name,
        end_timestamp=get_timestamp(),
        game_version='1.0.0',
        signature=signature,
    )

    res = client.post('/api/v1/score', json=score_sub1b.dict())
    assert res.status_code == 200

    # submission for user1 with score 1c and character 1b

    ticket1c = client.get('/api/v1/ticket').json()

    game = client.get(f'/api/v1/ticket/{ticket1c}')
    assert game.status_code == 200

    signature = _sign(score1c, user1, char2_name)

    score_sub1c = ScoreSubmission(
        ticket=ticket1c,
        user=user1,
        score=score1c,
        character_id=char1b,
        character_name=char2_name,
        end_timestamp=get_timestamp(),
        game_version='1.0.0',
        signature=signature,
    )

    res = client.post('/api/v1/score', json=score_sub1c.dict())
    assert res.status_code == 200

    # submission for user2

    ticket2 = client.get('/api/v1/ticket').json()

    game = client.get(f'/api/v1/ticket/{ticket2}')
    assert game.status_code == 200

    signature = _sign(score2, user2, char2_name)

    score_sub2 = ScoreSubmission(
        ticket=ticket2,
        user=user2,
        score=score2,
        character_id=char2,
        character_name=char2_name,
        end_timestamp=get_timestamp(),
        game_version='1.0.0',
        signature=signature,
    )

    res = client.post('/api/v1/score', json=score_sub2.dict())
    assert res.status_code == 200

    # submission for user3

    ticket3 = client.get('/api/v1/ticket').json()

    game = client.get(f'/api/v1/ticket/{ticket3}')
    assert game.status_code == 200

    signature = _sign(score3, user3, char3_name)

    score_sub3 = ScoreSubmission(
        ticket=ticket3,
        user=user3,
        score=score3,
        character_id=char3,
        character_name=char3_name,
        end_timestamp=get_timestamp(),
        game_version='1.0.0',
        signature=signature,
    )

    res = client.post('/api/v1/score', json=score_sub3.dict())
    assert res.status_code == 200

    # test highscore endpoint

    highscore_full = client.get(f'/api/v1/highscore', params={"user": user1, "character": char1a})
    assert highscore_full.status_code == 200
    assert highscore_full.json()['score'] == score1b

    highscore_usr = client.get(f'/api/v1/highscore', params={"user": user1})
    assert highscore_usr.status_code == 200
    assert highscore_usr.json()['score'] == score1c

    highscore_char = client.get(f'/api/v1/highscore', params={"character": char1a})
    assert highscore_char.status_code == 200
    assert highscore_char.json()['score'] == score3

    # test leaderboard endpoint

    leaderboard = client.get(f'/api/v1/leaderboard')
    assert leaderboard.status_code == 200
    assert len(leaderboard.json()) == 4
    assert leaderboard.json()[0]['score'] == score3

    leaderboard_char = client.get(f'/api/v1/leaderboard', params={"character": char1b})
    assert leaderboard_char.status_code == 200
    assert len(leaderboard_char.json()) == 2
    assert leaderboard_char.json()[0]['score'] == score1c

    # check that the ticket is invalidated after submission

    game = client.get(f'/api/v1/ticket/{ticket1a}')
    assert game.status_code == 404


def test_multiple_scores(test_db):
    char_name = 'Meowton'
    scores = {}

    # Do this 3 times with different users
    for i in range(0, 3):
        user = Account.create().address

        for c in range(0, 3):
            # Push 20 scores
            for _ in range(0, 20):
                score = random.randrange(0, 1500)
                ticket1a = client.get('/api/v1/ticket').json()

                game = client.get(f'/api/v1/ticket/{ticket1a}')
                assert game.status_code == 200

                signature = _sign(score, user, char_name)

                score_sub1a = ScoreSubmission(
                    ticket=ticket1a,
                    user=user,
                    score=score,
                    character_id=c,
                    character_name=char_name,
                    end_timestamp=get_timestamp(),
                    game_version='1.0.0',
                    signature=signature,
                )

                res = client.post('/api/v1/score', json=score_sub1a.dict())
                assert res.status_code == 200

                if c not in scores:
                    scores[c] = []
                scores[c].append(score)

            scores[c].sort()

            max_score = scores[c][-1]

            leaderboard = client.get(f'/api/v1/leaderboard', params={'character': c})
            assert leaderboard.status_code == 200
            assert len(leaderboard.json()) == i+1
            assert leaderboard.json()[0]['score'] == max_score
