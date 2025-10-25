from UI import Label, Card, Center, SoftBtn, Raw, AddSpace
from routes import ROUTES
from ENV import APP_NAME, FAVICON
from utils.Auth import isAuthenticated
from ENV import THEME_DEFAULT

def CompHero():
    with Card(
        "w-full h-fit p-10 rounded-3xl shadow-lg",
        styles=f"""
        background: linear-gradient(
            135deg, 
            {THEME_DEFAULT['primary']} 0%, 
            {THEME_DEFAULT['primary']}88 40%,
            white 60%, 
            {THEME_DEFAULT['secondary']} 100%
        );
        """
    ):
        with Raw.Div("grid grid-cols-1 sm:grid-cols-2"):
            with Center("max-w-3xl h-full gap-2 flex flex-col"):
                Label(APP_NAME + FAVICON, "text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl 2xl:text-9xl font-extrabold w-full")
                with Raw.RawRow("w-full"):
                    AddSpace()
                    Label(
                        "Start your projects in a nice way!",
                        "text-sm sm:text-lg p-1 mt-2 rounded-sm w-full md:w-[55%] italic",
                        styles=f"""
                            background: linear-gradient(
                                to right, 
                                {THEME_DEFAULT['secondary']}, 
                                transparent
                            );
                        """
                        )
                with Raw.RawRow("w-full justify-center items-center gap-2"):
                    if not isAuthenticated():
                        SoftBtn("Sign Up", link=ROUTES.SIGNUP, icon="add")
                        SoftBtn("Login", link=ROUTES.LOGIN, icon="person")
                    else:
                        SoftBtn("Dashboard", link=ROUTES.DASHBOARD, icon="dashboard")
                    AddSpace()