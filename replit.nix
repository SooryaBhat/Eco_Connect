{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.setuptools
    pkgs.python310Packages.wheel

    pkgs.python310Packages.flask
    pkgs.python310Packages.flask_login
    pkgs.python310Packages.jinja2
    pkgs.python310Packages.babel
    pkgs.python310Packages.flask_babel

    pkgs.python310Packages.sqlalchemy
    pkgs.python310Packages.pymysql
    pkgs.python310Packages.pillow
    pkgs.python310Packages.werkzeug
    pkgs.python310Packages.gunicorn
  ];
}
