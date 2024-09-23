from tortoise import Model, fields

# key_json={
# “title”:str,
# “kash”:[{
# “price”:decimal, 
# “minmax”:[{
# “min price”:decimal,
# ”max price”:decimal}]],
# ”difference”:decimal, 
# ”total amount”:decimal,
# “coins”: [
# {“BTC“:“USDT“,............“BTC“:“DOGE“}]
# “date”:str} 

class Price(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(50)
    price = fields.DecimalField(8, 2)
    max_price = fields.DecimalField(8, 2)
    min_price = fields.DecimalField(8, 2)
    date = fields.DatetimeField(auto_now_add=True)
    difference = fields.DecimalField(8, 2)
    total_amount = fields.DecimalField(8, 2)

    # Header_line=title,price,max price,min price, date ISOformat, difference, total amount
    def __str__(self):
        return f"id: {self.id}, title: {self.title}, price: {self.price}, max_price: {self.max_price}, min_price: {self.min_price}, date: {self.date.isoformat()}, difference: {self.difference}, total_amount: {self.total_amount}"
