import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SetStartLoading, SetStopLoading } from '../../store/app/app.action';
import { Store } from '@ngxs/store';
import { Observable, finalize, tap } from 'rxjs';

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {
  constructor(public store: Store) {}
  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      tap(() => {
        this.store.dispatch(new SetStartLoading());
      }),
      finalize(() => {
        this.store.dispatch(new SetStopLoading());
      })
    );
  }
}
