========
Examples
========

Initialize terminal
-------------------

.. code-block:: bash

    export RABBITMQ_HOST=
    export RABBITMQ_EXCHANGE=
    export RABBITMQ_USERNAME=
    export RABBITMQ_PASSWORD=
    export RABBITMQ_PORT=
    export RABBITMQ_VHOST=
    export RABBITMQ_QUEUE=
    export RABBITMQ_DURABLE_QUEUE=
    export MONGODB_CONNSTRING=
    export MONGODB_DATABASE=

Start DB storage (development)
------------------------------

.. code-block:: bash

    python -m eiffel_graphql_api.storage

Start DB storage (Docker)
-------------------------

.. code-block:: bash

    docker build -f Dockerfile.storage -t eiffel-storage .
    docker run \
        --name=storage \
        -e MONGODB_CONNSTRING=mongodb://username:secret@mongodb.example.com/eiffel \
        -e MONGODB_DATABASE=eiffel \
        -e RABBITMQ_HOST=rabbitmq.example.com \
        ...
        eiffel-storage

Start API (development server)
------------------------------

.. code-block:: bash

    ./entry_debug

Start API (Docker)
------------------

.. code-block:: bash

    docker build -f Dockerfile.graphql-api -t eiffel-graphql-api .
    docker run \
        --name=graphql-api \
        -p 5000:5000/tcp \
        -e MONGODB_CONNSTRING=mongodb://username:secret@mongodb.example.com/eiffel \
        -e MONGODB_DATABASE=eiffel \
        eiffel-graphql-api

Run tests
---------

.. code-block:: bash

    tox
