from apiclient import (
    APIClient,
    endpoint,
    retry_request,
    paginated,
    HeaderAuthentication,
    JsonResponseHandler,
    exceptions,
)
import tenacity
from apiclient.retrying import retry_if_api_request_error
from dotenv import load_dotenv
import json
import os

alma_api_base_url = "https://api-eu.hosted.exlibrisgroup.com/almaws/v1"

# env var
load_dotenv(os.path.join(os.getcwd(), ".env"))
alma_api_key = os.environ.get("ALMA_API_KEY")

alma_authentication_method = HeaderAuthentication(
    token=alma_api_key,
    parameter="apikey",
    scheme=None,
)

retry_decorator = tenacity.retry(
    retry=retry_if_api_request_error(status_codes=[429]),
    wait=tenacity.wait_fixed(2),
    stop=tenacity.stop_after_attempt(5),
    reraise=True,
)


@endpoint(base_url=alma_api_base_url)
class Endpoint:
    base = ""
    bibs = "bibs/{mms_id}"
    items = "items"


class Client(APIClient):
    
    @retry_request
    def dummy_search_item(self, format="alma", **param_kwargs):
        self.params = {**param_kwargs}
        data = open('dummy_item_data.json', 'r')
        result = json.load(data)
        return self._process_fetch_item(result,format)

    @retry_request
    def search_item(self, format="alma", **param_kwargs):
        """
        Alma Base request example
        https://api-eu.hosted.exlibrisgroup.com/almaws/v1/items?item_barcode=...
        
        Args
        format: alma|item-data|holding-data|call-number

        Ex Usage for barcode
        AlmaClient.search_item(item_barcode="...")
        AlmaClient.search_item(format="item-data",item_barcode="...")

        Returns
        A json object of item info
        """
        self.params = {**param_kwargs}
        result = self.get(Endpoint.items, params=self.params)
        if result:
            return self._process_fetch_item(result,format)
        return None
    
    def _process_fetch_item(self, result, format):
        if format == "alma":
            return result
        elif format == "holding-data":
            return result["holding_data"]
        elif format == "item-data":
            return result["item_data"]
        elif format == "call-number":
            return result["item_data"]["alternative_call_number"]


AlmaClient = Client(
    authentication_method=alma_authentication_method,
    response_handler=JsonResponseHandler,
)
