# fast_api

<!-- for Migration -->
<!-- the below line is for first time only to create files -->
# aerich init -t settings.database.TORTOISE_ORM

<!-- to migrate the fields in the models -->
# aerich migrate --name "enter the changes"

<!-- update the fields in the db -->
# aerich upgrade
