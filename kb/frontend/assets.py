# -*- coding: utf-8 -*-
"""
    kb.frontend.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    frontend application asset "pipeline"
"""

from flask_assets import Environment, Bundle

bower = "bower_components/"
foundation = "js/vendor/foundation/"

#: application css bundle
css_kb = Bundle("scss/kb.scss",
                    filters=["scss", "cssmin"], output="css/kb.css",
                    depends=['scss/*.scss'])

js_morris = Bundle("coffee/morris/morris.coffee",
                   "coffee/morris/morris.grid.coffee",
                   "coffee/morris/morris.hover.coffee",
                   "coffee/morris/morris.line.coffee",
                   "coffee/morris/morris.area.coffee",
                   "coffee/morris/morris.bar.coffee",
                   # "coffee/morris.donut.coffee"
                   filters="coffeescript", output="js/vendor/morris-custom-1.js")



shivs = Bundle(bower + "html5shiv/dist/html5shiv.min.js",
               filters="jsmin", output="js/vendor/shivs-1.js")


foundation = bower + "foundation/js/foundation/"

js_foundation = Bundle(foundation + "foundation.js",
                       foundation + "foundation.abide.js",
                       foundation + "foundation.accordion.js",
                       foundation + "foundation.alert.js",
                       # foundation + "foundation.clearing.js",
                       foundation + "foundation.dropdown.js",
                       foundation + "foundation.equalizer.js",
                       # foundation + "foundation.interchange.js",
                       # foundation + "foundation.joyride.js",
                       # foundation + "foundation.magellan.js",
                       foundation + "foundation.offcanvas.js",
                       # foundation + "foundation.orbit.js",
                       foundation + "foundation.reveal.js",
                       # foundation + "foundation.slider.js",
                       foundation + "foundation.tab.js",
                       foundation + "foundation.tooltip.js",
                       foundation + "foundation.topbar.js",
                       filters="jsmin", output="js/vendor/foundation-custom-1.js")

#: vendor js bundle
js_vendor = Bundle(bower + "jquery/dist/jquery.min.js",
                   bower + "jquery.placeholder/jquery.placeholder.min.js",
                   bower + "modernizr/modernizr.js",
                   bower + "fastclick/lib/fastclick.js",
                   bower + "lodash/dist/lodash.compat.min.js",
                   "js/vendor/zurb5-multiselect.js",
                   js_foundation,
                   js_morris,
                   filters="jsmin", output="js/vendor.min.js")

#: application js bundle
js_main = Bundle("coffee/*.coffee", filters="coffeescript", output="js/main.js")


def init_app(app):
    debug = app.debug
    webassets = Environment(app)
    # add foundation sass files to sass compiler paths
    webassets.config['SASS_LOAD_PATHS'] = ["../bower_components/foundation/scss/"]

    webassets.register('css_kb', css_kb)
    webassets.register('shivs', shivs)
    webassets.register('js_vendor', js_vendor)
    webassets.register('js_main', js_main)


    webassets.manifest = 'cache' if not debug else False
    webassets.cache = not debug
    webassets.debug = debug
