import abc


class BaseStorageClient(abc.ABC):
    @abc.abstractmethod
    def get_object(container: str, key: str) -> str:
        pass

    @abc.abstractmethod
    def upload_object(self, container: str, key: str, value: str) -> None:
        pass

    @abc.abstractmethod
    def delete_object(self, container: str, key: str) -> None:
        pass


class AzureStorageClient(BaseStorageClient):  # this class is not implemented yet
    ...


def get_storage_client() -> AzureStorageClient:
    return AzureStorageClient()  # how can we pass the connection string here?
