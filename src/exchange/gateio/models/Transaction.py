import pprint

class Transaction:
    def __init__(
        self,
        id,
        create_time,
        create_time_ms,
        currency_pair,
        side,
        role,
        amount,
        price,
        order_id,
        fee,
        fee_currency,
        point_fee,
        gt_fee,
        amend_text,
    ):
        self.id = float(id)
        self.create_time = create_time
        self.time = float(create_time_ms)/1000
        self.currency_pair = currency_pair
        self.side = side
        self.role = role
        self.qty = float(amount)
        self.price = float(price)
        self.order_id = order_id
        self.fee = fee
        self.fee_currency = fee_currency
        self.point_fee= point_fee
        self.gt_fee=gt_fee
        self.amend_text=amend_text

    def to_dict(self):
        return {
            "id": self.id,
            "create_time":self.create_time,
            "time":self.time,
            "currency_pair":self.currency_pair,
            "side":self.side,
            "role":self.role,
            "qty":self.qty,
            "price":self.price,
            "order_id":self.order_id,
            "fee":self.fee,
            "fee_currency":self.fee_currency,
            "point_fee":self.point_fee,
            "gt_fee":self.gt_fee,
            "amend_text":self.amend_text
        }
    
    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()
    
    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

@staticmethod
def editJsonResponse(response):
    edited_response = []
    for item in response:
        edited_item = Transaction(
            id=item.id,
            create_time=item.create_time,
            create_time_ms=item.create_time_ms,
            currency_pair=item.currency_pair,
            side=item.side,
            role=item.role,
            amount=item.amount,
            price=item.price,
            order_id=item.order_id,
            fee=item.fee,
            fee_currency=item.fee_currency,
            point_fee=item.point_fee,
            gt_fee=item.gt_fee,
            amend_text=item.amend_text,
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
