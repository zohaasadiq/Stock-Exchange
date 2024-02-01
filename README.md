### API App Views

#### StockDataView
- **Endpoint:** `/api/stocks/`
- **Methods:**
  - `POST`: Create a new stock entry.
  - `GET`: Retrieve all stock data.
- **Caching:** Utilizes caching for efficient retrieval with a cache expiration of 24 hours.

#### StockDataDetailView
- **Endpoint:** `/api/stocks/<str:ticker>/`
- **Methods:**
  - `GET`: Retrieve stock data for a specific ticker.
- **Caching:** Utilizes caching for efficient retrieval with a cache expiration of 24 hours.

#### TransactionCreateView
- **Endpoint:** `/api/transactions/`
- **Methods:**
  - `POST`: Create a new transaction entry.
- **Transaction Logic:**
  - Processes buy/sell transactions, updates user balance, and creates a transaction entry.
- **Error Handling:**
  - Handles insufficient balance and invalid transaction type errors.

#### TransactionListView
- **Endpoint:** `/api/transactions/<int:user_id>/`
- **Methods:**
  - `GET`: Retrieve a user's transaction history, ordered by timestamp.

#### TransactionRangeView
- **Endpoint:** `/api/transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/`
- **Methods:**
  - `GET`: Retrieve a user's transactions within a specified time range, ordered by timestamp.

### User App Views

#### CustomUserCreate
- **Endpoint:** `/users/`
- **Methods:**
  - `POST`: Create a new user.
- **Permissions:** Allows any user to create an account.

#### UserDataView
- **Endpoint:** `/users/<str:username>/`
- **Methods:**
  - `GET`: Retrieve user data for a specific username.
- **Caching:** Utilizes caching for efficient retrieval with a cache expiration of 24 hours.

### URL Configurations

#### API App URLs
- `/api/` is the base endpoint for API app views.

#### User App URLs
- `/users/` is the base endpoint for user app views.

### Models

#### NewUser
- Inherits from `AbstractBaseUser` and `PermissionsMixin`.
- Represents a user with fields: `username`, `balance`, `is_staff`, `is_active`.
- Custom manager for user creation.

#### StockData
- Represents stock data with fields: `ticker`, `open_price`, `close_price`, `high`, `low`, `volume`, `timestamp`.

#### Transactions
- Represents user transactions with fields: `transaction_id`, `user`, `ticker`, `transaction_type`, `transaction_volume`, `transaction_price`, `timestamp`.
- Transaction types: 'buy' and 'sell'.