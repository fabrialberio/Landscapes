pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'landscapes'
gnome = import('gnome')

subdir('ui')

gnome.compile_resources('landscapes',
  'landscapes.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  source_dir: meson.current_build_dir(),
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'landscapes.in',
  output: 'landscapes',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

landscapes_sources = [
  '__init__.py',
  'main.py',
  'parser.py',
  'window.py',
]

install_data(landscapes_sources, install_dir: moduledir)
