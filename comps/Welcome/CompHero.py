from UI import Label, Card, Center, SoftBtn, Raw, AddSpace, INIT_THEME
from routes import ROUTES
from ENV import APP_NAME, FAVICON
from ENV import QUOTE

def MessageFields():
    pass

async def CompHero():
    theme = await INIT_THEME()
    with Card(
        "w-full h-fit p-10 rounded-3xl shadow-lg",
        styles=f"""
        background: linear-gradient(
            135deg, 
            var(--q-primary) 0%, 
            var(--q-accent) 50%, 
            var(--q-secondary) 100%
        );
        """
    ):
        with Raw.Div("grid grid-cols-1 sm:grid-cols-2"):
            with Center("max-w-3xl h-full gap-2 flex flex-col"):
                Label(APP_NAME + FAVICON, "text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl 2xl:text-9xl font-extrabold w-full")
                if QUOTE:
                    with Raw.RawRow("w-full"):
                        AddSpace()
                        Label(
                            QUOTE,
                            "text-sm sm:text-lg p-1 mt-2 rounded-sm w-full md:w-[55%] italic",
                            styles=f"""
                                background: linear-gradient(
                                    to right, 
                                    var(--q-secondary), 
                                    transparent
                                );
                            """)
                with Raw.RawRow("w-full justify-center items-center gap-2"):
                    SoftBtn("Sign Up", link=ROUTES.SIGNUP, icon="add")
                    SoftBtn("Login", link=ROUTES.LOGIN, icon="person")
                    AddSpace()