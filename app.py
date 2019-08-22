from massbaystaffing import app
import os
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 84))
    app.run(debug=True, host='0.0.0.0', port=port)
