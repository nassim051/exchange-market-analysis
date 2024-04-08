import  os, sys, six
import src.interface.IMarketMan as imm
import src.exchange.gateio.models.OrderBook as modelOrderBook
import src.exchange.gateio.models.Transaction as modelTransaction
import src.exchange.gateio.models.My_trades as My_trades
import time
from src.exchange.gateio.github.gate_api.api_client import ApiClient
from src.exchange.gateio.github.gate_api.exceptions import ApiTypeError, ApiValueError  # noqa: F401
import src.exchange.gateio.models.Kline as Kline
STANDARD_TIME_TO_GATEIO_TIME_MAP = {
'minute5': '5m',
'minute15': '15m',
'minute30': '30m',
'hour1': '1h',
'hour4': '4h',
'hour8': '8h',
'hour12': '12h',
'day1': '1d',
'week1': '7d',
'month1': '30d'
}
class GateMarketMan(imm.IMarketMan):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def getTicker(self, **d):
        # Implement getTicker method for GateMarketMan
        pass
    
    def getIncrDepth(self, **d):
        # Implement getIncrDepth method for GateMarketMan
        pass

    def getTrades(self, **d):
        if 'size' in d:
            d['limit']=d.pop('size')
        if 'time' in d:
            d['_from']=d.pop('time')
        if "symbol" in d:
            currency_pair = d["symbol"]
            del d["symbol"]  
        else:
            raise KeyError("The 'd' dictionary does not contain the 'currency_pair' key")

        """Retrieve market trades  # noqa: E501

        You can use `from` and `to` to query by time range, or use `last_id` by scrolling page. The default behavior is by time range.  Scrolling query using `last_id` is not recommended any more. If `last_id` is specified, time range query parameters will be ignored.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_trades(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param int limit: Maximum number of records to be returned in a single list.  Default: 100, Minimum: 1, Maximum: 1000
        :param str last_id: Specify list staring point using the `id` of last record in previous list-query results
        :param bool reverse: Whether the id of records to be retrieved should be less than the last_id specified. Default to false.  When `last_id` is specified. Set `reverse` to `true` to trace back trading history; `false` to retrieve latest tradings.  No effect if `last_id` is not specified.
        :param int _from: Start timestamp of the query
        :param int to: Time range ending, default to current time
        :param int page: Page number
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: list[gate_api.Trade]
        :return: If the method is called asynchronously,
                 returns the request thread.
        """
        d['_return_http_data_only'] = True
        while True:
            try:
                response= self._list_trades_with_http_info(currency_pair, **d)  # noqa: E501
            except Exception as e:
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        return(modelTransaction.editJsonResponse(response))
    def _list_trades_with_http_info(self, currency_pair, **kwargs):  # noqa: E501
        """Retrieve market trades  # noqa: E501

        You can use `from` and `to` to query by time range, or use `last_id` by scrolling page. The default behavior is by time range.  Scrolling query using `last_id` is not recommended any more. If `last_id` is specified, time range query parameters will be ignored.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_trades_with_http_info(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param int limit: Maximum number of records to be returned in a single list.  Default: 100, Minimum: 1, Maximum: 1000
        :param str last_id: Specify list staring point using the `id` of last record in previous list-query results
        :param bool reverse: Whether the id of records to be retrieved should be less than the last_id specified. Default to false.  When `last_id` is specified. Set `reverse` to `true` to trace back trading history; `false` to retrieve latest tradings.  No effect if `last_id` is not specified.
        :param int _from: Start timestamp of the query
        :param int to: Time range ending, default to current time
        :param int page: Page number
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: tuple(list[gate_api.Trade], status_code(int), headers(HTTPHeaderDict))
        :return: If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['currency_pair', 'limit', 'last_id', 'reverse', '_from', 'to', 'page']
        all_params.extend(['async_req', '_return_http_data_only',
                          '_preload_content', '_request_timeout'])

        for k, v in six.iteritems(local_var_params['kwargs']):
            if k not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'" " to method list_trades" % k)
            local_var_params[k] = v
        del local_var_params['kwargs']
        # verify the required parameter 'currency_pair' is set
        if self.api_client.client_side_validation and (
            'currency_pair' not in local_var_params or local_var_params['currency_pair'] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `currency_pair` when calling `list_trades`"
            )  # noqa: E501

        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] > 1000
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list_trades`, must be a value less than or equal to `1000`"
            )  # noqa: E501
        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] < 1
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list_trades`, must be a value greater than or equal to `1`"
            )  # noqa: E501
        if (
            self.api_client.client_side_validation and 'page' in local_var_params and local_var_params[
                'page'] < 1
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `page` when calling `list_trades`, must be a value greater than or equal to `1`"
            )  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'currency_pair' in local_var_params and local_var_params['currency_pair'] is not None:  # noqa: E501
            query_params.append(('currency_pair', local_var_params['currency_pair']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'last_id' in local_var_params and local_var_params['last_id'] is not None:  # noqa: E501
            query_params.append(('last_id', local_var_params['last_id']))  # noqa: E501
        if 'reverse' in local_var_params and local_var_params['reverse'] is not None:  # noqa: E501
            query_params.append(('reverse', local_var_params['reverse']))  # noqa: E501
        if '_from' in local_var_params and local_var_params['_from'] is not None:  # noqa: E501
            query_params.append(('from', local_var_params['_from']))  # noqa: E501
        if 'to' in local_var_params and local_var_params['to'] is not None:  # noqa: E501
            query_params.append(('to', local_var_params['to']))  # noqa: E501
        if 'page' in local_var_params and local_var_params['page'] is not None:  # noqa: E501
            query_params.append(('page', local_var_params['page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        return self.api_client.call_api(
            '/spot/trades',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Trade]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
        )
        




    def getKline(self, **d):
        if 'size' in d:
            d['limit']=d.pop('size')
        if 'time' in d:
            d['_from']=d.pop('time')
        if "symbol" in d:
            d['interval']=STANDARD_TIME_TO_GATEIO_TIME_MAP[d.pop('type')]
        if "symbol" in d:
            currency_pair = d["symbol"]
            del d["symbol"]  
        else:
            raise KeyError("The 'd' dictionary does not contain the 'currency_pair' key")

        """Market candlesticks  # noqa: E501

        Maximum of 1000 points can be returned in a query. Be sure not to exceed the limit when specifying from, to and interval  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_candlesticks(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param int limit: Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected.
        :param int _from: Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified
        :param int to: End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time
        :param str interval: Interval time between data points. Note that `30d` means 1 natual month, not 30 days
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: list[list[str]]
        :return: If the method is called asynchronously,
                 returns the request thread.
        """
        d['_return_http_data_only'] = True
        return Kline.editJsonResponse(self.list_candlesticks_with_http_info(currency_pair, **d))  # noqa: E501

    def list_candlesticks_with_http_info(self, currency_pair, **kwargs):  # noqa: E501
        """Market candlesticks  # noqa: E501

        Maximum of 1000 points can be returned in a query. Be sure not to exceed the limit when specifying from, to and interval  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_candlesticks_with_http_info(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param int limit: Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected.
        :param int _from: Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified
        :param int to: End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time
        :param str interval: Interval time between data points. Note that `30d` means 1 natual month, not 30 days
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: tuple(list[list[str]], status_code(int), headers(HTTPHeaderDict))
        :return: If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['currency_pair', 'limit', '_from', 'to', 'interval']
        all_params.extend(['async_req', '_return_http_data_only',
                          '_preload_content', '_request_timeout'])

        for k, v in six.iteritems(local_var_params['kwargs']):
            if k not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'" " to method list_candlesticks" % k)
            local_var_params[k] = v
        del local_var_params['kwargs']
        # verify the required parameter 'currency_pair' is set
        if self.api_client.client_side_validation and (
            'currency_pair' not in local_var_params or local_var_params['currency_pair'] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `currency_pair` when calling `list_candlesticks`"
            )  # noqa: E501

        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] > 1000
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list_candlesticks`, must be a value less than or equal to `1000`"
            )  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'currency_pair' in local_var_params and local_var_params['currency_pair'] is not None:  # noqa: E501
            query_params.append(('currency_pair', local_var_params['currency_pair']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if '_from' in local_var_params and local_var_params['_from'] is not None:  # noqa: E501
            query_params.append(('from', local_var_params['_from']))  # noqa: E501
        if 'to' in local_var_params and local_var_params['to'] is not None:  # noqa: E501
            query_params.append(('to', local_var_params['to']))  # noqa: E501
        if 'interval' in local_var_params and local_var_params['interval'] is not None:  # noqa: E501
            query_params.append(('interval', local_var_params['interval']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/spot/candlesticks',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[list[str]]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
        )

    def getDepth(self, **d):
        if "symbol" in d:
            currency_pair = d["symbol"]
            del d["symbol"]  # Remove the key from the dictionary
            # Rest of your code using currency_pair_value
            # ...
        else:
            raise KeyError("The 'd' dictionary does not contain the 'currency_pair' key")

        """Retrieve order book  # noqa: E501

        Order book will be sorted by price from high to low on bids; low to high on asks  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_order_book(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param str interval: Order depth. 0 means no aggregation is applied. default to 0
        :param int limit: Maximum number of order depth data in asks or bids
        :param bool with_id: Return order book ID
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: gate_api.OrderBook
        :return: If the method is called asynchronously,
                 returns the request thread.
        """
        d['_return_http_data_only'] = True
        while True:
            try:
                response= self._list_order_book_with_http_info(currency_pair, **d)  # noqa: E501
            except Exception as e:
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        return modelOrderBook.editJsonResponse(response)
    def _list_order_book_with_http_info(self, currency_pair, **d):  # noqa: E501
        """Retrieve order book  # noqa: E501

        Order book will be sorted by price from high to low on bids; low to high on asks  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_order_book_with_http_info(currency_pair, async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Currency pair (required)
        :param str interval: Order depth. 0 means no aggregation is applied. default to 0
        :param int limit: Maximum number of order depth data in asks or bids
        :param bool with_id: Return order book ID
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: tuple(gate_api.OrderBook, status_code(int), headers(HTTPHeaderDict))
        :return: If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['currency_pair', 'interval', 'limit', 'with_id']
        all_params.extend(['async_req', '_return_http_data_only',
                          '_preload_content', '_request_timeout'])

        for k, v in six.iteritems(local_var_params['d']):
            if k not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'" " to method list_order_book" % k)
            local_var_params[k] = v
        del local_var_params['d']
        # verify the required parameter 'currency_pair' is set
        if self.api_client.client_side_validation and (
            'currency_pair' not in local_var_params or local_var_params['currency_pair'] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `currency_pair` when calling `list_order_book`"
            )  # noqa: E501

        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] < 1
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list_order_book`, must be a value greater than or equal to `1`"
            )  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'currency_pair' in local_var_params and local_var_params['currency_pair'] is not None:  # noqa: E501
            query_params.append(('currency_pair', local_var_params['currency_pair']))  # noqa: E501
        if 'interval' in local_var_params and local_var_params['interval'] is not None:  # noqa: E501
            query_params.append(('interval', local_var_params['interval']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'with_id' in local_var_params and local_var_params['with_id'] is not None:  # noqa: E501
            query_params.append(('with_id', local_var_params['with_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/spot/order_book',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OrderBook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
        )
        

    def my_trades(self, **kwargs):  # noqa: E501
        """List personal trading history  # noqa: E501

        Spot and margin trades are queried by default. If cross margin trades are needed, `account` must be set to `cross_margin`  You can also set `from` and(or) `to` to query by time range. If you don't specify `from` and/or `to` parameters, only the last 7 days of data will be retured. The range of `from` and `to` is not alloed to exceed 30 days.  Time range parameters are handled as order finish time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Retrieve results with specified currency pair
        :param int limit: Maximum number of records to be returned in a single list
        :param int page: Page number
        :param str order_id: Filter trades with specified order ID. `currency_pair` is also required if this field is present
        :param str account: Specify operation account. Default to spot and margin account if not specified. Set to `cross_margin` to operate against margin account.  Portfolio margin account must set to `cross_margin` only
        :param int _from: Start timestamp of the query
        :param int to: Time range ending, default to current time
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: list[gate_api.Trade]
        :return: If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        response= self.list_with_http_info(**kwargs)  # noqa: E501
        return My_trades.editJsonResponse(response)

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List personal trading history  # noqa: E501

        Spot and margin trades are queried by default. If cross margin trades are needed, `account` must be set to `cross_margin`  You can also set `from` and(or) `to` to query by time range. If you don't specify `from` and/or `to` parameters, only the last 7 days of data will be retured. The range of `from` and `to` is not alloed to exceed 30 days.  Time range parameters are handled as order finish time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param bool async_req: execute request asynchronously
        :param str currency_pair: Retrieve results with specified currency pair
        :param int limit: Maximum number of records to be returned in a single list
        :param int page: Page number
        :param str order_id: Filter trades with specified order ID. `currency_pair` is also required if this field is present
        :param str account: Specify operation account. Default to spot and margin account if not specified. Set to `cross_margin` to operate against margin account.  Portfolio margin account must set to `cross_margin` only
        :param int _from: Start timestamp of the query
        :param int to: Time range ending, default to current time
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :rtype: tuple(list[gate_api.Trade], status_code(int), headers(HTTPHeaderDict))
        :return: If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['currency_pair', 'limit', 'page', 'order_id', 'account', '_from', 'to']
        all_params.extend(['async_req', '_return_http_data_only',
                          '_preload_content', '_request_timeout'])

        for k, v in six.iteritems(local_var_params['kwargs']):
            if k not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'" " to method list" % k)
            local_var_params[k] = v
        del local_var_params['kwargs']

        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] > 1000
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list`, must be a value less than or equal to `1000`"
            )  # noqa: E501
        if (
            self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params[
                'limit'] < 1
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `limit` when calling `list`, must be a value greater than or equal to `1`"
            )  # noqa: E501
        if (
            self.api_client.client_side_validation and 'page' in local_var_params and local_var_params[
                'page'] < 1
        ):  # noqa: E501
            raise ApiValueError(
                "Invalid value for parameter `page` when calling `list`, must be a value greater than or equal to `1`"
            )  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'currency_pair' in local_var_params and local_var_params['currency_pair'] is not None:  # noqa: E501
            query_params.append(('currency_pair', local_var_params['currency_pair']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'page' in local_var_params and local_var_params['page'] is not None:  # noqa: E501
            query_params.append(('page', local_var_params['page']))  # noqa: E501
        if 'order_id' in local_var_params and local_var_params['order_id'] is not None:  # noqa: E501
            query_params.append(('order_id', local_var_params['order_id']))  # noqa: E501
        if 'account' in local_var_params and local_var_params['account'] is not None:  # noqa: E501
            query_params.append(('account', local_var_params['account']))  # noqa: E501
        if '_from' in local_var_params and local_var_params['_from'] is not None:  # noqa: E501
            query_params.append(('from', local_var_params['_from']))  # noqa: E501
        if 'to' in local_var_params and local_var_params['to'] is not None:  # noqa: E501
            query_params.append(('to', local_var_params['to']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['apiv4']  # noqa: E501
        return self.api_client.call_api(
            '/spot/my_trades',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Trade]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
        )
