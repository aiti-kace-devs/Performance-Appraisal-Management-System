import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, NavigationEnd, Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { BehaviorSubject, filter } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NavigationService {
  constructor(public router: Router) {
    this.router.events
      .pipe(
        // Filter the NavigationEnd events as the breadcrumb is updated only when the route reaches its end
        filter((event) => event instanceof NavigationEnd)
      )
      .subscribe((event) => {
        const root = this.router.routerState.snapshot.root;
        const breadcrumbs: MenuItem[] = [];
        this.addBreadcrumb([], breadcrumbs, root);
        // Emit the new hierarchy

        const unique = breadcrumbs.reduce<MenuItem[]>(
          (a, b) =>
            a.find(({ routerLink }) => routerLink === b.routerLink)
              ? a
              : [...a, b],
          // : a.concat(b as any),
          []
        );

        this.breadCrumbs$.next(unique);
      });
  }

  readonly breadCrumbs$ = new BehaviorSubject<MenuItem[]>([]);

  private addBreadcrumb(
    parentUrl: string[],
    breadcrumbs: MenuItem[],
    route?: ActivatedRouteSnapshot
  ) {
    if (route) {
      // Construct the route URL
      const routeUrl = parentUrl.concat(route.url.map((url) => url.path));

      // Add an element for the current route part
      if (route.data['breadcrumb']) {
        const breadcrumb = {
          label: route.data['breadcrumb'],
          routerLink: '/' + routeUrl.join('/'),
        };
        breadcrumbs.push(breadcrumb);
      }

      // Add another element for the next route part
      this.addBreadcrumb(routeUrl, breadcrumbs, route.firstChild!);
    }
  }
}
