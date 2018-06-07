from flask_script import Manager
from mainApp import create_app
from flask_migrate import MigrateCommand


app = create_app()
#创建manage管理入口
#数据迁移命令的基础
manage = Manager(app)

#添加db迁移的命令
manage.add_command('db',MigrateCommand)




manage.run()

