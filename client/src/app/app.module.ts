import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { AppComponent } from './app.component';
import { RouterOutlet } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AlertsModule } from './shared/alerts/alerts.module';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';

@NgModule({
  declarations: [AppComponent, MainLayoutComponent],
  imports: [
    CommonModule,
    RouterOutlet,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    AlertsModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
