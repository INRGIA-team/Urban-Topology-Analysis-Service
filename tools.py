import shlex
import subprocess
import os
import osmnx


def osm_tools(args):
    if type(args) == str:
        args = shlex.split(args)
    notepad = subprocess.Popen(args)
    notepad.wait()
    print(notepad.poll())


def osm_conversion(path_to_converter, infile, outfile):
    osm_tools([path_to_converter, infile, '-o=' + outfile])


def cut_area_by_osmium(path_to_osmium, infile, outfile, bbox='', polyfile=''):
    if bbox != '':
        osm_tools([path_to_osmium, 'extract', '-b', bbox, infile, '--overwrite', '-o', outfile])
    else:
        osm_tools([path_to_osmium, 'extract', '-p', polyfile, infile, '--overwrite', '-o', outfile])


def cut_area_by_converter(path_to_converter, infile, outfile, bbox='', polyfile=''):
    # osmconvertW64.exe MurinoLO_02.osm -b=30.442,60.0412,30.44343,60.049 --complete-ways -o=MurinoLO_01_01.osm
    if bbox != '':
        osm_tools([path_to_converter, infile, '-b=' + bbox, '--complete-ways', '-o=' + outfile])
    else:
        osm_tools([path_to_converter, infile, '-B=', polyfile, '--complete-ways', '-o=' + outfile])


def filtering_by_osmium(path_to_osmium, infile, outfile, tags):
    # 'osmium tags-filter rome.osm.pbf w/highway -o highways-in-rome.osm.pbf'
    osm_tools([path_to_osmium, 'tags-filter', infile, tags, '--overwrite', '-o', outfile])


def filtering_by_filter(path_to_filter, infile, outfile, tags):
    # './osmfilter norway.osm --keep="highway=primary =secondary waterway=river" >streets.osm'
    osm_tools([path_to_filter, infile, '--keep=', tags, '>', outfile])


def osm_sort(path_to_osmium, infile, outfile):
    # osmium sort input.osm.pbf -o output.osm.pbf
    osm_tools([path_to_osmium, 'sort', infile, '--overwrite', '-o', outfile])


def osm_concatenate(path_to_osmium, infile, outfile):
    # 'osmium cat -o dest.osm.pbf source.osm.pbf -t node -t way'
    osm_tools([path_to_osmium, 'cat', '--overwrite', '-o', outfile, infile, '-t', 'node', '-t', 'way'])


def osm_to_nx(infile, outfile='.\\outfile.osm', bbox='', polyfile='', tags='', osmconvert='.\\osmconvertW64.exe',
              osmium='.\\osmium.exe', temp_file_1='.\\tmp1.pbf', temp_file_2='.\\tmp2.pbf'):
    osm_conversion(osmconvert, infile, temp_file_1, )
    cut_area_by_osmium(osmium, temp_file_1, temp_file_2, bbox=bbox, polyfile=polyfile)
    filtering_by_osmium(osmium, temp_file_2, outfile, tags)
    return osmnx.graph_from_xml(outfile)


def main():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    osmconvert = dirname + '\\tools\\osmconvertW64.exe'
    osmfilter = dirname + '\\tools\\osmfilter.exe'
    osmium = dirname + '\\tools\\osmium.exe'
    infile = dirname + '\\samples\\OSM\\Perm.osm'
    temporary_file_1 = dirname + '\\samples\\OSM\\temporary\\Perm.pbf'
    temporary_file_2 = dirname + '\\samples\\OSM\\temporary\\Perm_the_cut.pbf'
    outfile = dirname + '\\tools\\samples\\Perm_roads.osm'
    bbox = '56.24,58.01,56.25,58.02'
    polyfile = ''
    tags = 'w/highway'

    osm_conversion(osmconvert, infile, temporary_file_1,)
    cut_area_by_osmium(osmium, temporary_file_1, temporary_file_2, bbox=bbox, polyfile=polyfile)
    filtering_by_osmium(osmium, temporary_file_2, outfile, tags)


if __name__ == '__main__':
    main()
