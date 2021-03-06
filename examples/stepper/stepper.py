import argparse
import gi
import os

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import GObject


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video-file",
    help="The path to the video file", required=True)
parser.add_argument("-l", "--landmark-file",
    help="The path to the shape predictor model", required=True)
args = parser.parse_args()
STEPPER_DIR = os.path.dirname(os.path.realpath(__file__))


class Player(Gtk.Window):
    def __init__(self, video_filepath, landmark_filepath, *args, **kwargs):
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL, *args, **kwargs)
        self.set_default_size(800, 600)

        self.video_filepath = video_filepath
        self.landmark_filepath = landmark_filepath

        gtksettings = Gtk.Settings.get_default()
        gtksettings.set_property("gtk-application-prefer-dark-theme", True)
        theme = gtksettings.get_property("gtk-theme-name")
        os.environ["GTK_THEME"] = theme + ":dark"

        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(STEPPER_DIR, "ui/example1.ui"))
        builder.add_from_file(os.path.join(STEPPER_DIR, "ui/menu.ui"))
        builder.connect_signals_full(self._builderConnectCb, self)

        self.viewer_box = builder.get_object("viewer_box")
        self.frame_label = builder.get_object("frame_label")
        self.add(self.viewer_box)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Player"

        menu_button = builder.get_object("menubutton")
        header_bar.pack_start(menu_button)

        self.set_titlebar(header_bar)
        self.connect("destroy", Gtk.main_quit)

        self.create_pipeline()
        self._frame_counter = 0

    def create_pipeline(self):
        spipeline = "filesrc name=source ! decodebin ! videoconvert ! "\
                    "cheesefacedetect name=face_detect ! "\
                    "videoconvert ! gtksink name=sink"

        self.pipeline = Gst.parse_launch(spipeline)
        self.source = self.pipeline.get_by_name("source")
        self.facedetect = self.pipeline.get_by_name("face_detect")
        self.sink = self.pipeline.get_by_name("sink")

        self.source.set_property("location", self.video_filepath)
        self.facedetect.set_property("display-bounding-box", True)
        self.facedetect.set_property("display-id", True)
        self.facedetect.set_property("display-landmark", True)
        self.facedetect.set_property("landmark", self.landmark_filepath)
        self.facedetect.set_property("use-hungarian", True)
        self.facedetect.set_property("hungarian-delete-threshold", 72)
        self.facedetect.set_property("scale-factor", 0.8)

        # GObject.timeout_add(300, self._duration_querier, self.pipeline)

        self.viewer = self.sink.get_property("widget")

        self.viewer_box.pack_start(self.viewer, True, True, 0)
        self.viewer_box.reorder_child(self.viewer, 0)
        self.viewer.show()

        self.pipeline.set_state(Gst.State.NULL)

    def _openCb(self, unused_item):
        dialog = Gtk.FileChooserDialog("Select a Blender file", self,
            Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(600, 400)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.source.set_property("location", filename)

        dialog.destroy()

    def _playCb(self, unused_button):
        self.pipeline.set_state(Gst.State.PLAYING)

    def _nextCb(self, unused_button):
        self.pipeline.set_state(Gst.State.PAUSED)
        step_event = Gst.Event.new_step(Gst.Format.BUFFERS, 1, 1.0, True, False)
        self.sink.send_event(step_event)
        self._frame_counter += 1
        self.frame_label.props.label = "Frame: %04d" % self._frame_counter

    def _builderConnectCb(self, builder, gobject, signal_name, handler_name,
                          connect_object, flags, user_data):
        id_ = gobject.connect(signal_name, getattr(self, handler_name))

    def _duration_querier(self, pipeline):
        position = pipeline.query_position(Gst.Format.TIME)
        print(position)
        return True

    def __pad_added_cb(self, decodebin, pad, converter):
        sinkpad = converter.get_static_pad("sink")
        pad.link(sinkpad)

Gst.init(None)
player = Player(args.video_file, args.landmark_file)
player.show_all()
Gtk.main()
