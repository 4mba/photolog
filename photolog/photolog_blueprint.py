from flask import Blueprint

photolog = Blueprint('photolog', __name__, 
						template_folder='../templates', static_folder='../static')

print 'photolog blueprint name : %s' % photolog.name
print 'photolog blueprint template folder : %s' % photolog.template_folder
print 'photolog blueprint static folder : %s' % photolog.static_folder