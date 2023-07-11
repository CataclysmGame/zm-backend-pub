import math

from eth_account.messages import encode_defunct
from loguru import logger
from web3 import Web3, Account

from app.core.cache import get_ticket
from app.core.models.score_submission import ScoreSubmission
from app.exceptions.anti_cheat_exception import AntiCheatException
from app.settings import settings
from app.util import get_timestamp


class AntiCheat:
    async def validate_submission(self, sub: ScoreSubmission) -> int:
        """
        Validates the score submission using various anti-cheat techniques.
        :param sub: The score submission to validate.
        :raises AntiCheatException: If the submission is invalid.
        :return: The game duration in seconds.
        """
        timestamp = get_timestamp()

        logger.debug('Validating score submission: {}', sub)

        ticket = await get_ticket(sub.ticket)
        sig = sub.signature

        if ticket is None:
            logger.error('Ticket not found: {}', sub.ticket)
            raise AntiCheatException('Ticket not found')

        if sig is None:
            logger.error('Game signature missing in submission: {}', sub.ticket)
            raise AntiCheatException('Game signature missing')

        start_ts = ticket['ts']

        duration = timestamp - start_ts

        server_duration = get_timestamp() - start_ts

        # duration_delta = math.fabs(duration - server_duration)

        if duration > server_duration:
            logger.error('Submission duration too high: {} / {}', duration, server_duration)
            raise AntiCheatException('Submitted timestamp is too far from the server reception timestamp')

        # Check signature
        skin_id = sub.character_skin or 'base'

        msg_hash = Web3.solidity_keccak(['address', 'string', 'string', 'uint256'],
                                        [sub.user, sub.character_name, skin_id, sub.score])
        sig_bytes = Web3.to_bytes(hexstr=sub.signature)
        rec_address = Account.recover_message(encode_defunct(msg_hash), signature=sig_bytes)

        if rec_address != settings.GAME_ADDRESS:
            logger.error('Invalid signature: {}', sub.signature)
            raise AntiCheatException('Invalid signature')

        return duration
