{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel

    # Flask + Extensions
    pkgs.python311Packages.flask
    pkgs.python311Packages.flask_login
    pkgs.python311Packages.sqlalchemy
    pkgs.python311Packages.werkzeug
    pkgs.python311Packages.pillow
    pkgs.python311Packages.pymysql
    pkgs.python311Packages.gunicorn

    # Babel (for translations)
    pkgs.python311Packages.babel
  ];
}
