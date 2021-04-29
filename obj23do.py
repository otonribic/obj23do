'''
Convert OBJ to 3DO format (General Wavefront to Dark Forces).
Python 3.7
Fish, 2021, oton.ribic@bug.hr
'''
import parsecl

def _showhelp():
    print('Converts OBJ 3D files (Wavefront generic) to 3DO format used by Dark Forces.')
    print('\nUsage:\n')
    print('obj23do inputfile [/O:outputfile] [/S:scale] [/C:color] [/REV] [/SH:shading]\n')
    print('inputfile    Input OBJ file with optional path')
    print('outputfile   Output 3DO file w/ optional path (default: add .3DO extension)')
    print('scale        Scale factor while converting (default: 1.000)')
    print('color        Color to be applied to the object (default: 32)')
    print('/REV         Reverse the face orientation. May be needed depending on the OBJ')
    print('shading      Shading to be used: GOURAUD (default) or FLAT')


def _parseobj(content, vscale=1.0):
    '''
    Parse the OBJ file content, return a list of vertices and triangular faces.
    '''
    lines = content.split('\n')
    # Define collectors
    vertices = []
    faces = []
    # Parse all
    for line in lines:
        if line.startswith('v '):
            # Vertex
            line = line.split(' ')[1:4]
            line = [float(k) * vscale for k in line]
            vertices.append(tuple(line))
        elif line.startswith('f '):
            # Face
            line = line.split(' ')[1:4]
            line = [k.partition('/')[0] for k in line]  # Take just vertex index!
            line = [int(k) - 1 for k in line]  # -1 because OBJ is 1-based!
            faces.append(tuple(line))
    # Return collectors
    return vertices, faces


def obj23do(inputfile,  # Input OBJ file with optional path
            outputfile=None,  # Optional output file
            vscale=1.0,  # Multiplier of vertex coordinates
            color=32,  # Color (from the palette) of the object
            shading='GOURAUD',  # Type of shading used
            reversefaces=False,  # Whether to reverse face directions from the OBJ
            ):
    # Determine output name if not given
    if not outputfile: outputfile = inputfile.rpartition('.')[0] + '.3do'

    # Load the OBJ
    print('Opening ' + inputfile)
    inph = open(inputfile, 'r', encoding='ascii')
    objvtx, objface = _parseobj(inph.read(), vscale)
    inph.close()
    print('OBJ loaded: {0} vertices, {1} faces'.format(len(objvtx), len(objface)))

    # Reverse faces if required
    if reversefaces:
        objvtx = [(a, c, b) for (a, b, c) in objvtx]

    # Get assembling the 3DO header
    c3do = []  # Line collector
    c3do.append('3DO 1.30')
    c3do.append('3DONAME GENERIC')
    c3do.append('OBJECTS 1')
    c3do.append('VERTICES {0}'.format(len(objvtx)))
    c3do.append('POLYGONS {0}'.format(len(objface)))
    c3do.append('PALETTE GENERIC.PAL')
    c3do.append('TEXTURES 0')
    # Object description
    c3do.append('OBJECT "GENERIC"')
    c3do.append('TEXTURE -1')

    # Add vertex information
    print('Adding vertex list')
    c3do.append('VERTICES {0}'.format(len(objvtx)))
    for id, vt in enumerate(objvtx):
        vtr = [round(c, 3) for c in vt]
        c3do.append('{0}: {1} {2} {3}'.format(id, vtr[0], vtr[1], vtr[2]))

    # Add face information
    print('Adding faces')
    c3do.append('TRIANGLES {0}'.format(len(objface)))
    for id, fc in enumerate(objface):
        c3do.append('{0}: {1} {2} {3} {4} {5}'.format(id, fc[0], fc[1], fc[2], color, shading))

    # Save all to a new file
    print('Writing output file ' + outputfile)
    outh = open(outputfile, 'w', encoding='ascii')
    outh.write('\n'.join(c3do))
    outh.close()
    print('Done')


### SELF-TEST & RUN
###################
if __name__ == '__main__':
    print('Convert OBJ to 3DO\n==================')
    import sys
#    sys.argv = ['', 'res\\pholder.obj', '/s:0.23']
    if len(sys.argv) <= 1:
        _showhelp()
        sys.exit(0)
    # Parse
    params = parsecl.parsecl(' '.join(sys.argv[1:]))
    # Set up function arguments
    inputfile = params['']
    outputfile = None
    if 'O' in params:
        outputfile = params['O']
    vscale = 1.0
    if 'S' in params:
        vscale = float(params['S'])
    color = 32
    if 'C' in params:
        color = int(params['C'])
    reversefaces = False
    if 'REV' in params:
        reversefaces = True
    shading = 'GOURAUD'
    if 'SH' in params:
        shading = params['SH'].upper()

    # Call the main function
    obj23do(inputfile=inputfile, outputfile=outputfile, vscale=vscale, color=color,
            reversefaces=reversefaces, shading=shading)
