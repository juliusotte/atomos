# Framework

## Objective
> In computer programming, a software framework is an abstraction in which software, providing generic functionality,
> can be selectively changed by additional user-written code, thus providing application-specific software. It provides
> a standard way to build and deploy applications and is a universal, reusable software environment that provides
> particular functionality as part of a larger software platform to facilitate the development of software applications,
> products and solutions. Software frameworks may include support programs, compilers, code libraries, toolsets, and
> application programming interfaces (APIs) that bring together all the different components to enable development of a
> project or system. (Wikipedia)

The objective of this event-driven framework is to provide a system of high-level abstraction components
that act as building blocks to develop performant, secure, resilient, distributed, and scalable microservices.

## Building Blocks
Besides the [system architecture](../architecture/architecture.md), the framework provides a variety of system
components that act as the building blocks to create microservices.

### Adapters
#### Repository
> Repositories are classes or components that encapsulate the logic required to access data sources. They centralize
> common data access functionality, providing better maintainability and decoupling the infrastructure or technology
> used to access databases from the domain model layer. (Microsoft)

Every repository defines a domain aggregate. The events and commands that are received by the service layer's message
bus will be handled by a unit of work (UOW), which defines an atomic update to the data persistence layer, in particular
the repository.

Thus, an abstract UOW depends on an abstract repository. Concrete UOW implementations (like a SQLAlchemy UOW) depend on
concrete repository implementations (like a SQLAlchemy repository implementation):

<img src='uow-repository-communication.drawio.svg' alt='uow-repository-communication' />

The framework provides an abstract base repository class that acts as an initial building block to develop custom
repository aggregates:

`atomos/core/adapters/repository/repository.py`
```python
class Repository(abc.ABC):
    collected_entities: Set[model.Model]

    def __init__(self):
        self.collected_entities = set()
```

A custom repository aggregate could then be defined as an abstract repository itself, depending on the abstract base
repository:

```python
class UserRepository(repository.Repository):
    def __init__(self):
        super().__init__()

    async def create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
    ):
        await self._create_user(username, password, email)
        self.collected_entities.add(user_model.User(username, password, email))

    async def get_user(self, username: Optional[str] = None, email: Optional[str] = None) -> Optional[user_model.User]:
        result = await self._get_user(username=username, email=email)
        if result:
            self.collected_entities.add(result)
        return result

    async def query_users(self, **criterion) -> Iterable[user_model.User]:
        results = await self._query_users(**criterion)
        if results:
            self.collected_entities.union(results)
        return results

    async def update_user(self, username: Optional[str], email: Optional[str], **update):
        await self._update_user(username, email, **update)

    async def delete_user(self, username: Optional[str] = None, email: Optional[str] = None):
        await self._delete_user(username=username, email=email)

    @abc.abstractmethod
    async def _create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_user(self, username: Optional[str], email: Optional[str]) -> Optional[user_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _query_users(self, **criterion) -> Iterable[user_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update_user(self, username: Optional[str], email: Optional[str], **update):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete_user(self, **criterion):
        raise NotImplementedError
```

The framework provides an abstract base SQLAlchemy repository that inherits the abstract base repository:

`atomos/core/adapters/repository/sqlalchemy_repository.py`
```python
class SQLAlchemyRepository(repository.Repository, abc.ABC):
    def __init__(self, session: Session = factory.DEFAULT_SESSION_FACTORY()):
        super().__init__()
        self.session: Session = session
```

The SQLAlchemy repository base can then be applied to create custom SQLAlchemy repository implementations:

```python
class SQLAlchemyUserRepository(
    sqlalchemy_repository.SQLAlchemyRepository,
    repository.IdentityRepository
):
    def __init__(self, session: Session = factory.DEFAULT_SESSION_FACTORY()):
        super().__init__(session)
        self.session = session

    async def _create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
    ):
        if not await self._get_user(username=username, email=email):
            self.session.add(user_model.User(username, password, email))

    async def _get_user(self, **criterion) -> Optional[user_model.User]:
        data = {
            k: v
            for k, v in criterion.items()
            if k in ['username', 'email']
            and v is not None
        }
        if not data:
            return None
        return self.session.query(user_model.User).filter_by(**data).first()

    async def _query_users(self, **criterion) -> Iterable[user_model.User]:
        return self.session.query(user_model.User).filter_by(**criterion).all()

    async def _update_user(self, username: Optional[str], email: Optional[str], **update):
        self.session.query(user_model.User).filter_by(username=username, email=email).update(**update)

    async def _delete_user(self, **criterion):
        result = await self._get_user(**criterion)
        if result:
            self.session.delete(result)
```

## References
- [Software framework (Wikipedia)](https://en.wikipedia.org/wiki/Software_framework)
- [Design the infrastructure persistence layer (Microsoft)](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)