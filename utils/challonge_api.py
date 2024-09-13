import aiohttp
import os
import traceback
from discord.ext.commands import Bot

BASE_URL = "https://api.challonge.com/v1/"


class ChallongeAPI:
    def __init__(self, client: Bot):
        self.api_key = os.environ.get("CHALLONGE_KEY")
        self.client = client
        logch = os.environ.get("LOGGING_CHANNEL")
        self.logchannel_id = int(logch) if logch else -1

    async def api_response(self, method: str, path: str, params: dict = {}):
        try:
            headers = {"Content-Type": "application/json"}

            params["api_key"] = self.api_key
            async with aiohttp.ClientSession(BASE_URL, headers=headers) as session:
                async with session.request(method, path, json=params) as resp:
                    response = await resp.json()
                    return response
        except Exception:
            logging_channel = await self.client.fetch_channel(self.logchannel_id)
            await logging_channel.send(
                f"Error while updating matches: {str(traceback.format_exc())}"
            )
            return None

    async def add_tournament(self, tournament_info):
        path = "tournaments.json"
        params = {
            "tournament": {
                "name": tournament_info.name,
                "game_name": "Competitive Programming",
                "prediction_method": 1,
                "tournament_type": [
                    "single elimination",
                    "double elimination",
                    "swiss",
                ][tournament_info.type],
                "private": "true",
            },
        }
        return await self.api_response("POST", path, params)

    async def bulk_add_participants(self, tournament_id, participants):
        path = f"tournaments/{tournament_id}/participants/bulk_add.json"

        params = {"participants": participants}
        return await self.api_response("POST", path, params)

    async def delete_tournament(self, tournament_id):
        path = f"tournaments/{tournament_id}.json"
        await self.api_response("DELETE", path)

    async def open_for_predictions(self, tournament_id):
        path = f"tournaments/{tournament_id}/open_for_predictions.json"

        return await self.api_response("POST", path)

    async def start_tournament(self, tournament_id):
        path = f"tournaments/{tournament_id}/start.json"

        return await self.api_response("POST", path)

    async def get_tournament_matches(self, tournament_id):
        path = f"tournaments/{tournament_id}/matches.json"
        return await self.api_response("GET", path)

    async def get_particiapnts_info(self, tournament_id):
        path = f"tournaments/{tournament_id}/participants.json"
        return await self.api_response("GET", path)

    async def post_match_results(self, tournament_id, match_id, scores, winner_id):
        path = f"tournaments/{tournament_id}/matches/{match_id}.json"
        params = {
            "match": {"scores_csv": scores, "winner_id": winner_id},
        }

        return await self.api_response("PUT", path, params)

    async def invalidate_match(self, tournament_id, match_id):
        path = f"tournaments/{tournament_id}/matches/{match_id}/reopen.json"

        return await self.api_response("POST", path)

    async def finish_tournament(self, tournament_id):
        path = f"tournaments/{tournament_id}/finalize.json"

        return await self.api_response("POST", path)
