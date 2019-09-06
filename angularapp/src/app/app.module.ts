import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import {MatGridListModule} from '@angular/material/grid-list';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BatteryListComponent } from './battery-list/battery-list.component';
import { BatteryDetailsComponent } from './battery-details/battery-details.component';


@NgModule({
  declarations: [
    AppComponent,
    BatteryListComponent,
    BatteryDetailsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatGridListModule,
    RouterModule.forRoot([
      { path: '', component: BatteryListComponent },
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
