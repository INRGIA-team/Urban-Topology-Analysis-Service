import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
import { Town } from '../interfaces/town';
import { Observable, of, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TownService {

  constructor(
    private http: HttpClient
  ) { }
  getTowns(): Observable<Town[]>{ //Observable - класс (из rxjs). Можно подписаться на изменение данных (.subscribe(func1, func2, func3)). (func1 - обработчик следующего значения, func2 - обработка ошибок, func3 - при завершении подачи данных) Нужен для ассинхронного изменения данных.
    return of(towns)
  }
  getTown(id: string): Observable<Town>{
    let town = towns.find(town=>town.id==id);
    return town ? of(town) : throwError('not found');
  }
}

const towns: Town[] = [
  {
    id:'1',
    name: 'Moscow',
    file:'/assets/maps/msc.osm',
    center: {
      lat: 55.7504461,
      lon: 37.6174943
    },
    districtFolder: 'moscow',
    districts: {city: [], children: [], subchildren: []}
  },{
    id:'2',
    name: 'Penza',
    file:'/assets/maps/pnz.osm',
    center: {
      lat: 53.1890, 
      lon: 45.0565
    },
    districts: {city: [], children: [], subchildren: []}
  },{
    id:'3',
    name: 'Saint-Petersburg',
    file:'/assets/maps/spb.osm',
    center: {
      lat: 59.9414, 
      lon: 30.3267
    },
    districts: {city: [], children: [], subchildren: []}
  }
]
