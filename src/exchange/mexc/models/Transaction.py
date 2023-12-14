import pprint

class Transaction:
    def __init__(
        self,
        T,
        m,
        q,
        p,
    ):
        self.time = float(T)
        self.isBuyerMaker=m
        self.qty = float(q)
        self.price = float(p)

    def to_dict(self):
        return {
            "time":self.time,
            "isBuyerMaker":self.isBuyerMaker,
            "qty":self.qty,
            "price":self.price,
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
                    T=item['T'],
        m=item['m'],
        q=item['q'],
        p=item['p'],
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
