# Authors:
#   George Pantelakis
#
# See the LICENSE file for legal information regarding use of this file.

"""compression module

This module has basic supported compression modules."""

from ..constants import CertificateCompressionAlgorithm
from .lists import getFirstMatching
from ..errors import TLSDecodeError

compression_algo_impls = {
    "brotli_compress": None,
    "brotli_decompress": None,
    "brotli_accepts_limit": None,
    "zstd_compress": None,
    "zstd_decompress": None,
    "zstd_accepts_limit": None
}

def choose_compression_send_algo(version, extension, valid_algos):
    if not extension or not version or version < (3, 4):
        return None

    chosen_compression_algo = None
    advertized_algos = extension.algorithms

    if not advertized_algos:
        raise TLSDecodeError("Empty algorithm list in compress_certificate "
                             "extension")

    if advertized_algos:
        supported_comp_algos = []
        for algo in valid_algos:
            try:
                supported_comp_algos.append(
                    getattr(CertificateCompressionAlgorithm, algo))
            except AttributeError:
                pass

        if supported_comp_algos:
            chosen_compression_algo = getFirstMatching(
                advertized_algos, supported_comp_algos)

    return chosen_compression_algo
