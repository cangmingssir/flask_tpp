from flask_script import Manager

from flask_migrate import MigrateCommand

from mainApp import create_app


app = create_app()
#创建manage管理入口
#数据迁移命令的基础
manager = Manager(app)

#添加db迁移的命令
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()

