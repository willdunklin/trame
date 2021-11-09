from trame.layouts import SinglePage
from trame.html import vtk, vuetify

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interacter factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for remote rendering factory initialization, not necessary for
# local rendering, but doesn't hurt to include it

import vtkmodules.vtkRenderingOpenGL2  # noqa


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
renderWindowInteractor.EnableRenderOff()

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def update_view(**kwargs):
    html_view.update()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("Hello Trame", on_ready=update_view)
layout.title.set_text("Hello Trame")

layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    ),
    vuetify.VBtn(
        vuetify.VIcon("mdi-crop-free"),
        icon=True,
        click="$refs.view.resetCamera()",
    ),
]

html_view = vtk.VtkLocalView(renderWindow)

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
