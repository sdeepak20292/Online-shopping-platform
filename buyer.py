# buyer_client.py
import grpc
import shopping_pb2
import shopping_pb2_grpc

class BuyerClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.market_stub = shopping_pb2_grpc.MarketStub(self.channel)

    def search_item(self, item_name, category):
        request = shopping_pb2.BuyerSearchRequest(item_name=item_name, category=category)
        items = self.market_stub.SearchItem(request)
        return items

    def buy_item(self, item_id, quantity, buyer_address):
        request = shopping_pb2.BuyerBuyRequest(item_id=item_id, quantity=quantity, buyer_address=buyer_address)
        return self.market_stub.BuyItem(request)

    def add_to_wishlist(self, item_id, buyer_address):
        request = shopping_pb2.BuyerWishlistRequest(item_id=item_id, buyer_address=buyer_address)
        return self.market_stub.AddToWishList(request)

    def rate_item(self, item_id, buyer_address, rating):
        request = shopping_pb2.BuyerRateRequest(item_id=item_id, buyer_address=buyer_address, rating=rating)
        return self.market_stub.RateItem(request)

if __name__ == '__main__':
    buyer_client = BuyerClient()

    while True:
        print("Choose a query:")
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            item_name = input("Enter item name (leave blank to display all items): ")
            category = input("Enter item category (ELECTRONICS, FASHION, OTHERS, ANY): ")
            search_result = buyer_client.search_item(item_name, category)
            print("Search Results:")
            for item in search_result:
                print(item)
        elif choice == "2":
            item_id = int(input("Enter item ID to buy: "))
            quantity = int(input("Enter quantity to purchase: "))
            buyer_address = input("Enter buyer's address (ip:port): ")
            buy_response = buyer_client.buy_item(item_id, quantity, buyer_address)
            print("Buy Item Response:", buy_response)
        elif choice == "3":
            item_id = int(input("Enter item ID to add to wishlist: "))
            buyer_address = input("Enter buyer's address (ip:port): ")
            wishlist_response = buyer_client.add_to_wishlist(item_id, buyer_address)
            print("Add to Wishlist Response:", wishlist_response)
        elif choice == "4":
            item_id = int(input("Enter item ID to rate: "))
            buyer_address = input("Enter buyer's address (ip:port): ")
            rating = int(input("Enter rating (1-5): "))
            rate_response = buyer_client.rate_item(item_id, buyer_address, rating)
            print("Rate Item Response:", rate_response)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
