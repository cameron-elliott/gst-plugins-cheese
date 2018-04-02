/*
 * GStreamer Plugins Cheese
 * Copyright (C) 2011 Laura Lucas Alday <lauralucas@gmail.com>
 * Copyright (C) 2018 Fabian Orccon <cfoch.fabian@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 * Alternatively, the contents of this file may be used under the
 * GNU Lesser General Public License Version 2.1 (the "LGPL"), in
 * which case the following provisions apply instead of the ones
 * mentioned above:
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#ifndef __GST_CHEESEFACEOVERLAY_H__
#define __GST_CHEESEFACEOVERLAY_H__

#include <gst/gst.h>
#include <cairo.h>
#include <graphene.h>
#include <graphene-gobject.h>
#include <gdk/gdk.h>
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <gst/cheese/face/cheesemultifacesprite.h>

G_BEGIN_DECLS

#define GST_TYPE_CHEESEFACEOVERLAY \
  (gst_cheese_face_overlay_get_type())
#define GST_CHEESEFACEOVERLAY(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST((obj),GST_TYPE_CHEESEFACEOVERLAY,GstCheeseFaceOverlay))
#define GST_CHEESEFACEOVERLAY_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST((klass),GST_TYPE_CHEESEFACEOVERLAY,GstCheeseFaceOverlayClass))
#define GST_IS_FACEOVERLAY(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE((obj),GST_TYPE_CHEESEFACEOVERLAY))
#define GST_IS_FACEOVERLAY_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE((klass),GST_TYPE_CHEESEFACEOVERLAY))

typedef struct _GstCheeseFaceOverlay GstCheeseFaceOverlay;
typedef struct _GstCheeseFaceOverlayClass GstCheeseFaceOverlayClass;

struct _GstCheeseFaceOverlay
{
  GstBin parent;

  GstPad *sinkpad, *srcpad;
  GstElement *overlay;
  guint64 frame_counter;

  GHashTable *faces;
  gulong buffer_probe_id;

  /* Properties */
  gchar *location;
  gchar *data;
  CheeseMultifaceSprite *multiface_sprite;
};

struct _GstCheeseFaceOverlayClass
{
  GstBinClass parent_class;
};

GType gst_cheese_face_overlay_get_type (void);

G_END_DECLS

#endif /* __GST_CHEESEFACEOVERLAY_H__ */
