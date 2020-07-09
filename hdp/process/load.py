from pathlib import Path
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
import gpxpy
from gpxpy import gpx

import pandas as pd

from hdp.struct.datatable import DataTable


def _get_file_name(path):
    if isinstance(path, Path):
        name = path.name
    else:
        name = Path(str(path)).name
    return name


# Team 1
def clean_up(datatable_list):
    pass


def load_csv(csv_files: list, params: dict = {}):
    """
    Read list of CSV files.

    Parameters
    ----------
    csv_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_csv function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    data_table_list = []
    exceptions = {}
    for path in csv_files:
        data_table = DataTable()
        name = _get_file_name(path)
        try:
            data_table.df = pd.read_csv(path, **params)
        except Exception as exc:
            exceptions[name] = str(exc)
        else:
            data_table.name = name
            data_table.path = path
            data_table_list.append(data_table)
    return data_table_list, exceptions


# Team 1
def load_json(json_files: list, params: dict = {}):
    """
    Read list of JSON files.

    Parameters
    ----------
    json_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_json function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    data_table_list = []
    exceptions = {}
    for path in json_files:
        data_table = DataTable()
        name = _get_file_name(path)
        try:
            data_table.df = pd.read_json(path, **params)
        except Exception as exc:
            exceptions[name] = str(exc)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions


# Team 1
def load_xlsx(xlsx_files: list, params: dict = {}):
    """
    Read list of xlsx files.

    Parameters
    ----------
    xlsx_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_excel function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    data_table = DataTable()

    for path in xlsx_files:
        try:
            data_table.df = pd.read_excel(path, **params)
            name = _get_file_name(path)

        except Exception as e:
            exceptions_dict[name] = str(e)

        else:
            data_table.name = name
            data_table_list.append(data_table)

    return data_table_list, exceptions_dict


# Team 1
def load_xls(xls_files: list, params: dict = {}):
    """
    Read list of xls files.

    Parameters
    ----------
    xls_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_excel function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    data_table = DataTable()

    for path in xls_files:
        try:
            data_table.df = pd.read_excel(path, **params)
            name = _get_file_name(path)

        except Exception as e:
            exceptions_dict[name] = str(e)

        else:
            data_table.name = name
            data_table_list.append(data_table)

    return data_table_list, exceptions_dict


def extract_tracks(gpx_parsed):  # I have to end it
    track_list = list()
    if len(gpx_parsed.tracks) != 0:
        for track in gpx_parsed.tracks:
            for segment in track.segments:
                for point in segment.points:
                    track_dict = dict()
                    track_dict["type"] = "Trackpoint"
                    track_dict["longitude"] = point.longitude
                    track_dict["elevation"] = point.elevation
                    track_dict["latitude"] = point.latitude
                    track_dict["time"] = point.time
                    track_list.append(track_dict)
    return track_list


def extract_waypoints(gtx_parsed):
    track_list = list()
    for waypoint in gtx_parsed.waypoints:
        waypoint_dict = dict()
        waypoint_dict["type"] = "Waypoint"
        waypoint_dict["longitude"] = waypoint.longitude
        waypoint_dict["elevation"] = waypoint.elevation
        waypoint_dict["latitude"] = waypoint.latitude
        track_list.append(waypoint_dict)
    return track_list


# Team 3
def load_gpx(gpx_files: list) -> Tuple[List[DataTable], Dict]:
    """
    Read list of gpx files

    Parameters
    ------------
    gpx_files: list of paths to .gpx files

    Returns
    -----------
    List with DataTable objects and dictonary with exceptions
    """
    exception_dict = {}
    data_table_list = []
    try:
        for path in gpx_files:
            data_table = DataTable()
            name = _get_file_name(path)
            with (open(path, "r")) as file:
                gpx_parsed = gpxpy.parse(file)
            waypoints = extract_waypoints(gpx_parsed)
            tracks = extract_tracks(gpx_parsed)
            points = tracks + waypoints
            data_table.df = pd.DataFrame(points)
            data_table.name = name
            data_table_list.append(data_table)
    except Exception as e:
        exception_dict[name] = str(e)
    else:
        data_table.name = name
        data_table_list.append(data_table)
    print(data_table_list[0].df)
    return data_table_list, exception_dict


def extract_one_field_data(trackpoint) -> Dict:
    """

    :param trackpoint:
    :return: Not nested point values
    """
    point = {single_element.name: single_element.text
             for single_element in trackpoint.children
             if isinstance(single_element, Tag) and len(single_element.findChildren()) == 0}
    return point


def extract_nested_values(trackpoint) -> Dict:
    point = {}
    for element in trackpoint.children:
        if isinstance(element, Tag) and len(element.findChildren()) > 1:
            for value in element.children:
                if isinstance(value, NavigableString):
                    point[value.name] = value.string
                elif isinstance(value, Tag):
                    point[value.name] = value.text.strip()
    return point


# Team 3
def load_tcx(tcx_files: List) -> Tuple[List, Dict]:
    """
    Read list of tcx files
    :param tcx_files : List
        List of path to tcx
    :return:
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

pass
    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    for path in tcx_files:
        try:
            data_table = DataTable()
            activites = []
            name = _get_file_name(path)
            with (open(path, "r")) as file:
                activity = BeautifulSoup(file, "lxml")
            for trackpoint in activity.find_all("trackpoint"):
                point = extract_one_field_data(trackpoint)
                nested_data = extract_nested_values(trackpoint)
                point = {**point, **nested_data}
                activites.append(point)
            data_table.df = pd.DataFrame(activites)
        except Exception as e:
            exceptions_dict[name] = str(e)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions_dict


# Team 4
def load_jpg(jpg_files: list, params: dict = {}):
    pass


load_gpx(["home-work.gpx", "sample.gpx"])
