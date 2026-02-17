import { Routes } from '@angular/router';
import { PolicyDashboardComponent } from './components/policy-dashboard/policy-dashboard.component';

export const routes: Routes = [
  {
    path: '',
    component: PolicyDashboardComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
];
