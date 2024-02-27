# seller_server.py
import grpc
import shopping_pb2
import shopping_pb2_grpc
from concurrent import futures

class MarketServicer(shopping_pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = []
        self.items = []

    def RegisterSeller(self, request, context):
        # Implement logic to register seller
        # Check if the seller_address is already registered
        for seller in self.sellers:
            if seller.address == request.seller_address:
                return shopping_pb2.SellerRegistrationResponse(message="FAIL")

        # Add seller to the list if not registered
        self.sellers.append(shopping_pb2.Seller(address=request.seller_address, uuid=request.uuid))
        print(f"Seller join request from {request.seller_address}[ip:port], uuid = {request.uuid}")
        return shopping_pb2.SellerRegistrationResponse(message="SUCCESS")

    def SellItem(self, request, context):
        # Implement logic to add item to the market
        # Generate a unique item id, update seller_address, etc.
        item_id = len(self.items) + 1
        item = shopping_pb2.Item(
            id=item_id,
            price=request.price,
            name=request.name,
            category=request.category,
            description=request.description,
            quantity_remaining=request.quantity_remaining,
            seller_address=request.seller_address,
            rating=0.0  # Initial rating
        )

        self.items.append(item)
        print(f"Sell Item request from {request.seller_address}")
        return item

    def UpdateItem(self, request, context):
        # Implement logic to update item details
        for item in self.items:
            if item.id == request.id and item.seller_address == request.seller_address:
                # Update item details
                item.price = request.price
                item.quantity_remaining = request.quantity_remaining
                print(f"Update Item {request.id}[id] request from {request.seller_address}")
                return item

        # Item not found or not owned by the seller
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Item not found or not owned by the seller.")
        return shopping_pb2.Item()

    def DeleteItem(self, request, context):
        # Implement logic to delete item
        for i, item in enumerate(self.items):
            if item.id == request.id and item.seller_address == request.seller_address:
                # Remove item from the list
                del self.items[i]
                print(f"Delete Item {request.id}[id] request from {request.seller_address}")
                return item

        # Item not found or not owned by the seller
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Item not found or not owned by the seller.")
        return shopping_pb2.Item()

    def DisplaySellerItems(self, request, context):
        # Implement logic to display seller items
        seller_items = [item for item in self.items if item.seller_address == request.seller_address]
        print(f"Display Items request from {request.seller_address}")
        return seller_items

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
