from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView


class PromotionsView(ListCreateAPIView):
    ...

class PromotionsDetailsId(RetrieveUpdateDestroyAPIView):
    ...


class PromotionsDetailsIdRate(CreateAPIView):
    ...


