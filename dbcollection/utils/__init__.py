from __future__ import print_function
from .string_ascii import str_to_ascii, ascii_to_str, convert_str_ascii, convert_ascii_str
from .url_download import url_get_filename, download_file, check_file_integrity_md5, remove_file
from .file_extraction import extract_file
from .file_load import load_matlab, load_json, load_pickle


def download_extract_all(urls, md5sum, dir_save, clean_cache=False, verbose=True):
    """Download urls + extract files to disk.

    Download + extract all url files to disk. If clean_cache is
    True, it removes the download files.

    Parameters
    ----------
    urls : list
        List of URL paths.
    md5sum : list
        List of md5 checksum strings for each url.
    dir_save : str
        Directory path to store the data.
    clean_cache : bool
        Remove downloaded files and keep only the extracted data.
    verbose : bool
        Display messages on screen.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Check if urls is a str
    if isinstance(urls, str):
        urls = [urls]

    # download + extract data and remove temporary files
    for i, url in enumerate(urls):
        if verbose:
            print('Download url ' + str(i+1) + '/' + str(len(urls)))

        # get download save filename
        fname_save = url_get_filename(url, dir_save)

        # download file
        download_file(url, dir_save, fname_save, verbose)

        # check md5 sum (if available)
        if any(md5sum):
            check_file_integrity_md5(fname_save, md5sum)

        # extract file
        extract_file(fname_save, dir_save, verbose)

        # remove downloaded file (if triggered by the user)
        if clean_cache:
            remove_file(fname_save)
