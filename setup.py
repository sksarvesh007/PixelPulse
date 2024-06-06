from cx_Freeze import setup, Executable

setup(

    name="PixelPulse",

    version="1.0",

    description="Your application description",

    executables=[Executable("main.py")],

)  