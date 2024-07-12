"""
iso.py

This file, if and when complete ;-), contains all the class definitions of boxes that are specified in ISO/IEC 14496-12.
Additionally a class to represent the MP4 file that contains the MP4 boxes has been defined.
A box_factory function has also been defined, primarily to minimise coupling between modules.

"""

import logging


from .boxes.builder import build_box
from .m4a_summary import Summary

# Supported box
# 'ftyp', 'pdin', 'moov', 'mvhd', 'meta', 'trak', 'tkhd', 'tref', 'trgr', 'edts', 'elst', 'mdia',
# 'mdhd', 'hdlr', 'elng', 'minf', 'vmhd', 'smhd', 'hmhd', 'nmhd', 'dinf', 'dref', 'url ', 'urn ',
# 'stbl', 'stsd', 'stts', 'ctts', 'cslg', 'stsc', 'stsz', 'stz2', 'stco', 'co64', 'stss', 'stsh',
# 'padb', 'stdp', 'sdtp', 'sbgp', 'sgpd', 'subs', 'saiz', 'saio', 'udta', 'mvex', 'mehd', 'trex',
# 'leva', 'moof', 'mfhd', 'traf', 'tfhd', 'trun', 'tfdt', 'mfra', 'tfra', 'mfro', 'mdat', 'free',
# 'skip', 'cprt', 'tsel', 'strk', 'stri', 'strd', 'iloc', 'ipro', 'rinf', 'sinf', 'frma', 'schm',
# 'xml ', 'pitm', 'iref', 'meco', 'mere', 'styp', 'sidx', 'ssix', 'prft', 'avc1', 'hvc1', 'avcC',
# 'hvcC', 'btrt', 'pasp', 'mp4a', 'ac-3', 'ec-3', 'esds', 'dac3', 'dec3', 'ilst', 'data', 'pssh',
# 'senc'
# Not supported
# 'sthd', 'iinf', 'bxml', 'fiin', 'paen', 'fire', 'fpar', 'fecr', 'segr', 'gitn', 'idat'


class SimpleMp4File(object):
    def __init__(self, filename):
        self.filename = filename
        self.type = "file"
        self.children = []
        self._init_children()

    def _init_children(self):
        is_end = False
        try:
            with open(self.filename, "rb") as f:
                while not is_end:
                    cbox = build_box(f, self)
                    self.children.append(cbox)
                    if cbox.size == 0:
                        is_end = True
                    if len(f.read(4)) != 4:
                        is_end = True
                    else:
                        f.seek(-4, 1)
        except Exception as e:
            print(
                f"[error] {self.filename} error after child {len(self.children)} for {e}"
            )

    def check_moov_is_header(self):
        if len(self.children) < 3:
            return False
        box0 = self.children[0]
        box1 = self.children[1]
        if box0.type == "ftyp" and box1.type == "moov":
            return True
        if box0.type == "moov":
            return True
        return False


class Mp4File(object):
    """mp4分析文件类"""

    def __init__(self, filename):
        self.filename = filename
        self.type = "file"
        self.children = []
        is_end = False
        try:
            with open(filename, "rb") as f:
                while not is_end:
                    cbox = build_box(f, self)
                    self.children.append(cbox)
                    if cbox.size == 0:
                        is_end = True
                    if len(f.read(4)) != 4:
                        is_end = True
                    else:
                        f.seek(-4, 1)
            self._generate_samples_from_moov()
            self._generate_samples_from_moofs()
        except Exception as e:
            # catch exception in case we can continue
            logging.exception(f"error in {filename} after child {len(self.children)}")

    def _generate_samples_from_moov(self):
        """在 mp4 识别 mdat"""
        mdats = [mbox for mbox in self.children if mbox.type == "mdat"]
        # generate a sample list if there is a moov that contains traks N.B only ever 0,1 moov boxes
        if [box for box in self.children if box.type == "moov"]:
            moov = [box for box in self.children if box.type == "moov"][0]
            traks = [tbox for tbox in moov.children if tbox.type == "trak"]
            sample_list = []
            for trak in traks:
                trak_id = [box for box in trak.children if box.type == "tkhd"][
                    0
                ].box_info["track_ID"]
                timescale = [
                    box
                    for box in [box for box in trak.children if box.type == "mdia"][
                        0
                    ].children
                    if box.type == "mdhd"
                ][0].box_info["timescale"]
                samplebox = [
                    box
                    for box in [
                        box
                        for box in [box for box in trak.children if box.type == "mdia"][
                            0
                        ].children
                        if box.type == "minf"
                    ][0].children
                    if box.type == "stbl"
                ][0]
                chunk_offsets = [
                    box
                    for box in samplebox.children
                    if box.type == "stco" or box.type == "co64"
                ][0].box_info["entry_list"]
                sample_size_box = [
                    box
                    for box in samplebox.children
                    if box.type == "stsz" or box.type == "stz2"
                ][0]
                if sample_size_box.box_info["sample_size"] > 0:
                    sample_sizes = [
                        {"entry_size": sample_size_box.box_info["sample_size"]}
                        for i in range(sample_size_box.box_info["sample_count"])
                    ]
                else:
                    sample_sizes = sample_size_box.box_info["entry_list"]
                sample_to_chunks = [
                    box for box in samplebox.children if box.type == "stsc"
                ][0].box_info["entry_list"]
                s2c_index = 0
                next_run = 0
                sample_idx = 0
                for i, chunk in enumerate(chunk_offsets, 1):
                    if i >= next_run:
                        samples_per_chunk = sample_to_chunks[s2c_index][
                            "samples_per_chunk"
                        ]
                        s2c_index += 1
                        next_run = (
                            sample_to_chunks[s2c_index]["first_chunk"]
                            if s2c_index < len(sample_to_chunks)
                            else len(chunk_offsets) + 1
                        )
                    chunk_dict = {
                        "track_ID": trak_id,
                        "chunk_ID": i,
                        "chunk_offset": chunk["chunk_offset"],
                        "samples_per_chunk": samples_per_chunk,
                        "chunk_samples": [],
                    }
                    sample_offset = chunk["chunk_offset"]
                    for j, sample in enumerate(
                        sample_sizes[sample_idx : sample_idx + samples_per_chunk],
                        sample_idx + 1,
                    ):
                        chunk_dict["chunk_samples"].append(
                            {
                                "sample_ID": j,
                                "size": sample["entry_size"],
                                "offset": sample_offset,
                            }
                        )
                        sample_offset += sample["entry_size"]
                    sample_list.append(chunk_dict)
                    sample_idx += samples_per_chunk
            # sample_list could be empty, say, for mpeg-dash initialization segment
            if sample_list:
                # sort by chunk offset to get interleaved list
                sample_list.sort(key=lambda k: k["chunk_offset"])
                for mdat in mdats:
                    mdat_sample_list = [
                        sample
                        for sample in sample_list
                        if mdat.start_of_box
                        < sample["chunk_offset"]
                        < (mdat.start_of_box + mdat.size)
                    ]
                    if len(mdat_sample_list):
                        mdat.box_info["message"] = "Has samples."
                    mdat.sample_list = mdat_sample_list

    def _generate_samples_from_moofs(self):
        """
        generate samples within mdats of media segments for fragmented mp4 files
        media segments are 1 moof (optionally preceded by an styp) followed by 1 or more contiguous mdats
        I've only ever seen 1 mdat in a media segment though
        """
        i = 0
        while i < len(self.children) - 1:
            if self.children[i].type == "moof":
                moof = self.children[i]
                media_segment = {"moof_box": moof, "mdat_boxes": []}
                sequence_number = [
                    mfhd for mfhd in moof.children if mfhd.type == "mfhd"
                ][0].box_info["sequence_number"]
                while (
                    i < len(self.children) - 1 and self.children[i + 1].type == "mdat"
                ):
                    media_segment["mdat_boxes"].append(self.children[i + 1])
                    i += 1
                # I've only ever seen 1 traf in a moof, but the standard says there could be more
                data_offset = 0
                for j, traf in enumerate(
                    [tbox for tbox in moof.children if tbox.type == "traf"]
                ):
                    # read tfhd, there will be one
                    tfhd = [hbox for hbox in traf.children if hbox.type == "tfhd"][0]
                    trak_id = tfhd.box_info["track_id"]
                    if "base_data_offset" in tfhd.box_info:
                        data_offset = tfhd.box_info["base_data_offset"]
                    elif tfhd.box_info["default_base_is_moof"]:
                        data_offset = media_segment["moof_box"].start_of_box
                    elif j > 0:
                        # according to spec. should be set end of data for last fragment
                        pass
                    else:
                        base_data_offset = media_segment["moof_box"].start_of_box
                    for k, trun in enumerate(
                        [rbox for rbox in traf.children if rbox.type == "trun"], 1
                    ):
                        if "data_offset" in trun.box_info:
                            data_offset += trun.box_info["data_offset"]
                        run_dict = {
                            "sequence_number": sequence_number,
                            "track_ID": trak_id,
                            "run_ID": k,
                            "run_offset": data_offset,
                            "sample_count": trun.box_info["sample_count"],
                            "run_samples": [],
                        }
                        has_sample_size = (
                            True if trun.flags & 0x0200 == 0x0200 else False
                        )
                        for l, sample in enumerate(trun.box_info["samples"], 1):
                            if not has_sample_size:
                                sample_size = tfhd.box_info["default_sample_size"]
                            else:
                                sample_size = sample["sample_size"]
                            run_dict["run_samples"].append(
                                {
                                    "sample_ID": l,
                                    "size": sample_size,
                                    "offset": data_offset,
                                }
                            )
                            data_offset += sample_size
                        for mdat in media_segment["mdat_boxes"]:
                            if (
                                mdat.start_of_box < run_dict["run_offset"]
                                and (mdat.start_of_box + mdat.size) >= data_offset
                            ):
                                mdat.box_info["message"] = "Has samples."
                                mdat.sample_list.append(run_dict)
            i += 1

    def read_bytes(self, offset, num_bytes):
        with open(self.filename, "rb") as f:
            f.seek(offset)
            bytes_read = f.read(num_bytes)
        f.close()
        return bytes_read

    def get_summary(self):
        if not self.summary:
            self.summary = Summary(self)
        return self.summary.data

    def search_boxes_for_type(self, box_type):
        type_matches = []
        for box in self.children:
            if box.type == box_type:
                type_matches.append(box)
            if box.children:
                type_matches += box.search_child_boxes_for_type(box_type)
        return type_matches


# Box classes
