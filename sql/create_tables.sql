DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS plans;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id    VARCHAR(20) PRIMARY KEY,
    gender         VARCHAR(10),
    senior_citizen INT,
    partner        VARCHAR(5),
    dependents     VARCHAR(5),
    tenure         INT
);

CREATE TABLE plans (
    plan_id         SERIAL PRIMARY KEY,
    contract        VARCHAR(20),
    payment_method  VARCHAR(50),
    monthly_charges NUMERIC(8,2),
    total_charges   NUMERIC(10,2)
);

CREATE TABLE subscriptions (
    subscription_id  SERIAL PRIMARY KEY,
    customer_id      VARCHAR(20) REFERENCES customers(customer_id),
    plan_id          INT REFERENCES plans(plan_id),
    phone_service    VARCHAR(5),
    internet_service VARCHAR(20),
    streaming_tv     VARCHAR(5),
    streaming_movies VARCHAR(5),
    churn            VARCHAR(5)
);