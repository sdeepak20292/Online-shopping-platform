# buyer_seller_client.py
import grpc
import shopping_pb2
import shopping_pb2_grpc

class BuyerSellerClient:
    def __init__(self, client_type):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.client_type = client_type
        if client_type == 'buyer':
            self.market_stub = shopping_pb2_grpc.BuyerStub(self.channel)
        elif client_type == 'seller':
            self.market_stub = shopping_pb2_grpc.MarketStub(self.channel)
        else:
            raise ValueError("Invalid client type. Use 'buyer' or 'seller'.")

    def register_seller(self, seller_address, uuid):
        request = shopping_pb2.SellerRegistrationRequest(seller_address=seller_address, uuid=uuid)
        return self.market_stub.RegisterSeller(request)

    def sell_item(self, item):
        return self.market_stub.SellItem(item)

    def update_item(self, item):
        return self.market_stub.UpdateItem(item)

    def delete_item(self, item_id, seller_address):
        request = shopping_pb2.Item(id=item_id, seller_address=seller_address)
        return self.market_stub.DeleteItem(request)

    def display_seller_items(self, seller_address):
        request = shopping_pb2.SellerRegistrationRequest(seller_address=seller_address)
        items = self.market_stub.DisplaySellerItems(request)
        for item in items:
            print(item)


def run_buyer_seller_client():
    client_type = input("Enter client type ('buyer' or 'seller'): ").lower()
    client = BuyerSellerClient(client_type)

    while True:
        print("\nChoose an option:")
        print("1. Register Seller")
        print("2. Sell Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Display Seller Items")

        print("0. Exit")

        choice = input("Enter your choice (0-9): ")

        if choice == '0':
            break
        elif choice == '1':
            seller_address = input("Enter seller address: ")
            uuid = input("Enter seller UUID: ")
            response = client.register_seller(seller_address, uuid)
            print(response.message)
        elif choice == '2':
            item = shopping_pb2.Item(
                price=float(input("Enter item price: ")),
                name=input("Enter item name: "),
                category=input("Enter item category: "),
                description=input("Enter item description: "),
                quantity_remaining=int(input("Enter item quantity: ")),
                seller_address=input("Enter seller address: "),
                rating=float(input("Enter item rating: "))
            )
            response = client.sell_item(item)
            print("Sell Item Response:", response)
        elif choice == '3':
            item_id = int(input("Enter item ID to update: "))
            item = shopping_pb2.Item(
                id=item_id,
                price=float(input("Enter new price: ")),
                quantity_remaining=int(input("Enter new quantity: ")),
                seller_address=input("Enter seller address: ")
            )
            response = client.update_item(item)
            print("Update Item Response:", response)
        elif choice == '4':
            item_id = int(input("Enter item ID to delete: "))
            seller_address = input("Enter seller address: ")
            response = client.delete_item(item_id, seller_address)
            print("Delete Item Response:", response)
        elif choice == '5':
            seller_address = input("Enter seller address: ")
            client.display_seller_items(seller_address)
        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

if __name__ == '__main__':
    run_buyer_seller_client()
