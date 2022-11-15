export interface townBounds{
    maxlat: string,
    maxlon: string, 
    minlat: string,
    minlon: string
}

export enum districtLevels{
  city = 'city',
  children = 'children',
  subchildren = 'subchildren'
}

export interface _center{
  lat: number,
  lon: number
}

export type _coordinates = L.LatLngTuple[][] | L.LatLngTuple[]

export interface _district{
    type: string,
    properties: {
      osm_id: number,
      local_name: string,
    },
    geometry: {
      type: string,
      coordinates: _coordinates[],
    }
}
  
  export interface _distBounds{
    type: string,
    crs: {
      type: string,
      properties: {
        name: string
      }
    },
    features: _district[]
  }

export type _districts = {
  [key in districtLevels]: _district[]
}

export interface Town{
    id: string,
    name: string,
    map?: any,
    file?: string,
    districtFolder?: string,
    image?: string,
    // bounds?: townBounds,
    center: _center,
    districts: _districts
}