## Available links for API Endpoints:

1. GET /api/check/ - List all checks
2. GET /api/check/<int:pk>/ - Retrieve a single check by ID
3. PUT /api/check/<int:pk>/ - Update a single check by ID
4. PATCH /api/check/<int:pk>/ - Partially update a single check by ID
5. DELETE /api/check/<int:pk>/ - Delete a single check by ID
6. POST /api/point/<int:point_id>/check/ - Create a new check for a specific point
7. GET /api/printer/<int:printer_id>/check/ - List all checks for a specific printer
8. GET /api/print/<filename>/ - View the PDF of a specific check by file name


## Commands for run app in docker:

1. git clone git@github.com:ston1997/check.git   ## clone repository
2. docker exec -it check_api_backend python manage.py migrate --noinput   ## migrate
3. docker exec -it check_api_backend python manage.py loaddata fixtures/check.json   ## load fixtures
4. docker exec -it check_api_backend python manage.py createsuperuser   ## create superuser
5. docker-compose up --build   ## build and up docker container