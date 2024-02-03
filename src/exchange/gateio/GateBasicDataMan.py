
import pytest, os, sys, six
import src.interface.IBasicDataMan as ibdm
import src.exchange.gateio.models.TradingPairs as modelTradingPairs
import time
from .github.gate_api.api_client import ApiClient
from .github.gate_api.exceptions import ApiTypeError, ApiValueError  # noqa: F401



class GateBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def getcurrencyPairs(self):
        # Implement the method here
        pass

    def getAccuracyInfo(self):
        kwargs={}
        """List all currency pairs supported  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_currency_pairs(async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: list[gate_api.CurrencyPair]
        :return: If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        while True:
                try:
                    response= self._list_currency_pairs_with_http_info(**kwargs)  # noqa: E501            
                except Exception:
                    print('An exeption occured:'+Exception)
                    print("l'm going to sleep for 15 seconde")
                    time.sleep(15)
                else:
                    break
        return modelTradingPairs.editJsonResponse(response)
    

    def getRatio(self, **d):
        # Implement the method here
        pass

    def getWithdrawConf(self, **d):
        # Implement the method here
        pass

    def getTimestamp(self):
        # Implement the method here
        pass
    def _list_currency_pairs_with_http_info(self, **kwargs):  # noqa: E501
        """List all currency pairs supported  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_currency_pairs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: tuple(list[gate_api.CurrencyPair], status_code(int), headers(HTTPHeaderDict))
        :return: If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = []
        all_params.extend(['async_req', '_return_http_data_only',
                          '_preload_content', '_request_timeout'])

        for k, v in six.iteritems(local_var_params['kwargs']):
            if k not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'" " to method list_currency_pairs" % k)
            local_var_params[k] = v
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/spot/currency_pairs',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CurrencyPair]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
        )


