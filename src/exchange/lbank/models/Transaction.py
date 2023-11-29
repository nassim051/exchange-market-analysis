import pprint

class Transaction:
    def __init__(self, time, qty, id, price, isBuyerMaker):
        self.time=time
        self.qty=float(qty)
        self.id=id
        self.price=price
        self.isBuyerMaker=isBuyerMaker
    def to_dict(self):
        return {
            "time":self.time,
            "qty":self.qty,
            "price":self.price,
            "id":self.id,
            "isBuyerMaker":self.isBuyerMaker
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
    for item in response['data']:
        edited_item = Transaction(
            time=item['time'],
            qty=item['qty'],
            price=item['price'], 
            id=item['id'],
            isBuyerMaker=item['isBuyerMaker']
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
