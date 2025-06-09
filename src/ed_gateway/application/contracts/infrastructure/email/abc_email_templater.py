from abc import abstractmethod


class ABCEmailTemplater:
    @abstractmethod
    def welcome_consumer(self, consumer_name: str) -> str: ...

    @abstractmethod
    def welcome_driver(self, driver_name: str) -> str: ...

    @abstractmethod
    def welcome_business(self, business_name: str) -> str: ...
