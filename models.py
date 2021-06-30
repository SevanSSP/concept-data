from pydantic import BaseModel, validator
from typing import Optional, List, Union


class HullGeometry(BaseModel):
    """
    Hull geometry definition

    Parameters
    ----------
    main_radius : float
        Radius of outer main hull (m)
    height : float
        Hull depth/height (m)
    symmetry : str
        Model symmetry code
    bilgebox_rz : list
        Coordinate pairs (radius from center line vs. height above baseline) defining the shape of the bilgebox.
    cutouts : list, optional
        Azimuth (degrees) and width (degrees) of bilgebox cut outs.
    moonpool_rz : list, optional
        Coordinate pairs (radius from center line vs. height above baseline) defining the shape of the moonpool.
    max_element_length : float, optional
        Maximum length of elements in panel model (m)
    """
    main_radius: float
    height: float
    symmetry: str
    bilgebox_rz: List[List[float]]
    cutouts: Optional[List[List[Union[float, bool]]]]
    moonpool_rz: Optional[List[List[float]]]

    @validator("symmetry")
    def valid_symmetry_code(cls, v):
        if v not in ("xz", "xzyz"):
            raise ValueError("Invalid symmetry code. Use 'xz' or 'xzyz'.")
        return v


class LoadingCondition(BaseModel):
    """
    Loading condition data

    Parameters
    ----------
    draft : float
        Draft (m)
    gm : float
        Metacentric height (m)
    xcg : float
        Centre of gravity x-coordinate (m)
    ycg : float
        Centre of gravity y-coordinate (m)
    vcg : float
        Vertical centre of gravity (m)
    mass : float
        Mass (kg)
    rixx : float
        Radii of gyration about the x-axis (m)
    riyy : float
        Radii of gyration about the y-axis (m)
    rizz : float
        Radii of gyration about the z-axis (m)
    cd : float
        Drag coefficient (-)
    ca : float
        Added mass coefficient (-)
    damping_matrix : list, optional
        Linear damping matrix
    restoring_matrix : list, optional
        Restoring stiffness matrix
    moonpool_damping_ratio : float, optional
        Moonpool damping as fraction of critical damping (-)
    """
    draft: float
    gm: float
    xcg: float
    ycg: float
    vcg: float
    mass: float
    rixx: float
    riyy: float
    rizz: float
    cd: float
    ca: float
    damping_matrix: Optional[List[List[float]]] = None
    restoring_matrix: Optional[List[List[float]]] = None
    moonpool_damping_ratio: Optional[float] = None


class WaveCondition(BaseModel):
    """
    Wave condition data

    Parameters
    ----------
    water_depth : float
        Water depth (m)
    spectrum : str
        Type of wave energy model spectrum e.g. 'jonswap'
    hs : float
        Significant wave height (m)
    tp : float
        Spectral peak period (s)
    gamma : float, optional
        Spectral peak enhancement factor (-)
    sa : float, optional
        Spectral width factor for wave periods larger than `tp` (-)
    sb : float, optional
        Spectral width factor for wave periods smaller than `tp` (-)
    """
    water_depth: float
    spectrum: str
    hs: float
    tp: float
    gamma: Optional[float] = 1.0
    sa: Optional[float] = 0.07
    sb: Optional[float] = 0.09

    @validator("gamma")
    def gamma_geq_one(cls, v):
        if v < 1.:
            raise ValueError("The peak enhancement factor shall not be lower than 1.")
        return v

    @validator("spectrum")
    def valid_spectrum(cls, v):
        if v not in ("pm", "jonswap", "torsethaugen", "simplified torsethaugen"):
            raise ValueError(f"The spectrum type '{v}' is invalid.")
        raise v


class HydraInput(BaseModel):
    """
    Input to radiation diffraction calculations
    """
    hull: HullGeometry
    loading_condition: LoadingCondition
    environmental_condition: WaveCondition

