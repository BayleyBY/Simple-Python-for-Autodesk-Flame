"""
Script Name: Add View Transform Track
Script Version: 1.0
Flame Version: 2027
Written by: Bryan Bayley
Creation Date: 08.13.26

Description:
Adds a new video track to the selected sequences and puts a Colour Management
gap effect on it, switched from its default Colour Transform mode to View
Transform. Gives a sequence a display transform that sits over the picture
below it without touching any of the existing segments.

The effect covers the picture only. Black heads and tails are found by scanning
the existing tracks for the first and last real picture segment - gaps and
colour sources such as black leaders are ignored - and the new track is cut down
to that range. A sequence with no identifiable picture gets an effect spanning
the whole track instead.

The new track goes directly below each sequence's topmost track, which puts the
view transform between the footage and the graphics above it. This is measured
per sequence, so a selection mixing three- four- and five-track sequences still
lands the new track second from the top in all of them. A single-track sequence
has nothing to sit below, so it gets its new track on top.

Limitation: the graphics have to be on a single track when the script is run.
The new track always lands below the topmost track, so a sequence carrying two
or more graphics tracks gets the view transform in between them rather than
under all of them. Run the script before stacking further graphics tracks, or
move the new track down by hand afterwards.

The effect is left at Flame's defaults for Tagged Colour Space, View and
Display, so it follows the project's colour management settings.

Menus:
Right-click a sequence in the Media Panel -> Sequence... -> Add View Transform Track
"""

import traceback

import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Add View Transform Track"
FOLDER = "Sequence..."

# The gap/segment flavour of the effect. "Source Colour Mgmt" is a separate
# source-side effect and is not what a gap takes.
EFFECT_TYPE = "Colour Mgmt"

# The effect is created in "Colour Transform" mode - this is what it becomes.
EFFECT_MODE = "View Transform"


def message_box(message):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(SCRIPT_NAME)
    msg.setText(message)
    msg.exec()


def scope_sequence(selection):
    for item in selection:
        if isinstance(item, flame.PySequence):
            return True
    return False


def gap_segment(track):
    """The single Gap segment of an empty track, or None if the track is not
    empty. A freshly created track always holds exactly one Gap."""
    if len(track.segments) == 1 and track.segments[0].type == "Gap":
        return track.segments[0]
    return None


def new_track(version):
    """Add a track directly below the topmost track, so an overlay track such
    as a title or burn-in stays above the view transform. A single-track
    sequence has nothing to sit below, so its new track goes on top.

    create_track() takes a 1-based insert index (-1 appends on top, 0 raises
    "Invalid track index"), so landing above the track at 0-based position i
    means inserting at i + 2. The track below the topmost one is at 0-based
    len(tracks) - 2, which lands the new track at index len(tracks).
    """
    count = len(version.tracks)

    if count < 2:
        print("%s: adding the new track on top" % SCRIPT_NAME)
        return version.create_track(-1)

    print("%s: adding the new track below the top track (V%d)"
          % (SCRIPT_NAME, count))
    return version.create_track(count)


def is_picture(segment):
    """False for the gaps and black leaders that top and tail a sequence.

    A black head or tail is a colour source, which carries no media, so an
    empty file path separates it from real picture.
    """
    if segment.type == "Gap":
        return False
    try:
        if not str(segment.file_path):
            return False
    except Exception:
        pass
    return True


def picture_range(version):
    """(start, end) record PyTimes spanning every picture segment in the
    version, or None when no picture is found.

    Every position here comes from the same sequence's record space, so the
    frame numbers are directly comparable.
    """
    start = None
    end = None

    for track in version.tracks:
        for segment in track.segments:
            if not is_picture(segment):
                continue
            if start is None or segment.record_in.frame < start.frame:
                start = segment.record_in
            if end is None or segment.record_out.frame > end.frame:
                end = segment.record_out

    if start is None or end is None:
        return None
    return (start, end)


def trim_gap_to_range(track, gap, start, end):
    """Cut the new track's gap down to the picture range and return the
    segment covering it, or None when it cannot be found."""
    gap_start = gap.record_in.frame
    gap_end = gap.record_out.frame

    if start.frame > gap_start:
        track.cut(cut_time=start)
    if end.frame < gap_end:
        track.cut(cut_time=end)

    # Clamped, so a picture range reaching past the gap still resolves.
    target = max(start.frame, gap_start)
    for segment in track.segments:
        if segment.record_in.frame <= target < segment.record_out.frame:
            return segment
    return None


def add_track_with_view_transform(clip):
    # create_track() belongs to PyVersion, so a version has to be named even
    # though single-version sequences are the normal case. versions[-1] is the
    # topmost one - versions[0] is the bottom of the stack.
    version = clip.versions[-1]

    # Measure the picture before adding the track, so the new track's own
    # full-length gap is not scanned as part of the sequence.
    picture = picture_range(version)

    track = new_track(version)
    if track is None:
        raise RuntimeError("Flame did not return a new track.")

    gap = gap_segment(track)
    if gap is None:
        raise RuntimeError("The new track has no gap segment to hold the effect.")

    if picture is None:
        print("%s: no picture found - covering the whole track" % SCRIPT_NAME)
    else:
        start, end = picture
        covered = trim_gap_to_range(track, gap, start, end)
        if covered is None:
            print("%s: could not isolate the picture - covering the whole track"
                  % SCRIPT_NAME)
        else:
            gap = covered
            print("%s: covering %s to %s" % (SCRIPT_NAME, str(start), str(end)))

    effect = gap.create_effect(EFFECT_TYPE)
    if effect is None:
        raise RuntimeError("Could not create a %s effect on the new track." % EFFECT_TYPE)

    effect.mode = EFFECT_MODE


def add_view_transform_track(selection):
    failed = []

    for clip in selection:
        if not isinstance(clip, flame.PySequence):
            continue

        clip_name = str(clip.name)[1:-1]
        print("%s: ----- '%s' -----" % (SCRIPT_NAME, clip_name))

        try:
            add_track_with_view_transform(clip)
            print("%s: added a %s track to '%s'" % (SCRIPT_NAME, EFFECT_MODE, clip_name))
        except Exception:
            print("%s: ERROR while adding a track to '%s':" % (SCRIPT_NAME, clip_name))
            traceback.print_exc()
            failed.append(clip_name)

    if failed:
        message_box(
            "No View Transform track was added to:\n\n"
            + "\n".join(failed)
            + "\n\nSee the Flame shell for details."
        )


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Add View Transform Track",
                    "isVisible": scope_sequence,
                    "execute": add_view_transform_track
                }
            ]
        }
    ]
