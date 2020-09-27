import os
Import('env')

extJars = [
    'example1.jar',
    'example2.jar',
    # Etc
]

rpmJars = [
    'example1.jar',
    'example2.jar',
    # Etc
]

cln = env.Clone()

cln.Replace( JAVACLASSPATH = [] )
cln.Append( JAVACLASSPATH = [ os.path.join(env['EXTERNAL_JAVA'], elem) for elem in extJars ] )
cln.Append( JAVACLASSPATH = [ os.path.join(env['RPM_JAVA'], elem) for elem in rpmJars ] )
# Etc

buildDir = 'build'

cln.Java( buildDir,
    [
        'org',
    ],
    JAVAVERSION = env['JAVA_VERSION']
)

resources = []

sources = \
    Glob('org/proj/apps/Editor/images/*') + \
    Glob('org/proj/apps/Viewer/images/*') + \
    Glob('org/proj/utils/swing/images/*')
    
sources = [ source.get_path() for source in sources ]
targets = [ os.path.join(buildDir, source) for source in sources ]

for source, target in map(None, sources, targets):
    resources.append(
        Command(
            target,
            source,
            Copy( '$TARGET', '$SOURCE' ),
        )
    )

archive = cln.Jar(os.path.join(env['JAR_DIR'], 'proj'),
    [
        buildDir,
    ],
    JARCHDIR = Dir( buildDir ),
)

cln.Depends( archive, resources )

# Force a complete clean
Clean( archive, buildDir )
