import type { IconKey } from './icons';

export interface NavItem {
  label: string;
  href: string;
  permission?: string; // hidden when the admin lacks it (UI only; backend enforces)
}

export interface NavSection {
  title: string | null;
  icon: IconKey;
  items: NavItem[];
}

export const NAV_SECTIONS: NavSection[] = [
  // 1. Dashboards (Direct link)
  { title: null, icon: 'home', items: [{ label: 'Dashboards', href: '/dashboard' }] },

  // 2. Declare Result (Direct link - Top Priority Operation)
  { title: null, icon: 'check', items: [{ label: 'Declare Result', href: '/dashboard/results/publish' }] },

  // 3. Starline Management (Dropdown)
  {
    title: 'Starline Management',
    icon: 'clock',
    items: [
      { label: 'Game Name', href: '/dashboard/markets/starline' },
      { label: 'Game Rates', href: '/dashboard/rates' },
      { label: 'Bid History', href: '/dashboard/simulations/history?market=starline' },
      { label: 'Declare Result', href: '/dashboard/results/publish?market=starline' },
      { label: 'Result History', href: '/dashboard/results/history?market=starline' },
      { label: 'Game Sell Report', href: '/dashboard/reports/game-statistics?market=starline' },
      { label: 'Game Winning Report', href: '/dashboard/reports/simulation-statistics?market=starline' },
      { label: 'Winning Prediction', href: '/dashboard/reports/number-frequency?market=starline' },
    ],
  },

  // 4. Gali Disawar (Dropdown)
  {
    title: 'Gali Disswar',
    icon: 'calendar',
    items: [
      { label: 'Game Name', href: '/dashboard/markets/gali-disawar' },
      { label: 'Game Rates', href: '/dashboard/rates' },
      { label: 'Bid History', href: '/dashboard/simulations/history?market=gali-disawar' },
      { label: 'Declare Result', href: '/dashboard/results/publish?market=gali-disawar' },
      { label: 'Result History', href: '/dashboard/results/history?market=gali-disawar' },
      { label: 'Sell Report', href: '/dashboard/reports/game-statistics?market=gali-disawar' },
      { label: 'Winning Report', href: '/dashboard/reports/simulation-statistics?market=gali-disawar' },
      { label: 'Winning Prediction', href: '/dashboard/reports/number-frequency?market=gali-disawar' },
    ],
  },

  // 5. Report Management (Dropdown)
  {
    title: 'Report Management',
    icon: 'chart',
    items: [
      { label: 'Users Bid History', href: '/dashboard/simulations/history' },
      { label: 'Customer Sell Report', href: '/dashboard/reports/game-statistics' },
      { label: 'Winning Report', href: '/dashboard/reports/simulation-statistics' },
      { label: 'Transfer Point Report', href: '/dashboard/wallet-activity/transactions' },
      { label: 'Bid Win Report', href: '/dashboard/simulations' },
      { label: 'Withdraw Report', href: '/dashboard/wallet-activity/credit-requests' },
      { label: 'Auto Deposit History', href: '/dashboard/wallet-activity/activity' },
    ],
  },

  // 6. Winning Prediction (Direct link)
  { title: null, icon: 'sliders', items: [{ label: 'Winning Prediction', href: '/dashboard/reports/number-frequency' }] },

  // 7. Wallet Management (Dropdown)
  {
    title: 'Wallet Management',
    icon: 'coin',
    items: [
      { label: 'Fund Request', href: '/dashboard/wallet-activity/credit-requests' },
      { label: 'Withdraw Request', href: '/dashboard/wallet-activity/credit-requests' },
      { label: 'Amount Added By Admin', href: '/dashboard/wallet-activity/credits' },
      { label: 'Add Fund (User Wallet)', href: '/dashboard/wallet-activity/credits' },
      { label: 'Bid Revert', href: '/dashboard/wallet-activity/activity' },
      { label: 'Autopay Transaction', href: '/dashboard/wallet-activity/transactions' },
    ],
  },

  // 8. User Management (Direct link)
  { title: null, icon: 'users', items: [{ label: 'User Management', href: '/dashboard/students' }] },

  // 9. Games Management (Dropdown - Main Matka Markets)
  {
    title: 'Games Management',
    icon: 'market',
    items: [
      { label: 'Game Name', href: '/dashboard/markets/matka' },
      { label: 'All Markets', href: '/dashboard/markets' },
      { label: 'Market Schedule', href: '/dashboard/schedule' },
      { label: 'Game Rates', href: '/dashboard/rates' },
    ],
  },

  // 10. Game & Numbers (Dropdown)
  {
    title: 'Game & Numbers',
    icon: 'sliders',
    items: [
      { label: 'Single Digit', href: '/dashboard/game-config/SINGLE' },
      { label: 'Jodi Digit', href: '/dashboard/game-config/JODI' },
      { label: 'Single Pana', href: '/dashboard/game-config/SINGLE_PANNA' },
      { label: 'Double Pana', href: '/dashboard/game-config/DOUBLE_PANNA' },
      { label: 'Tripple Pana', href: '/dashboard/game-config/TRIPLE_PANNA' },
      { label: 'Half Sangam', href: '/dashboard/game-config/HALF_SANGAM' },
      { label: 'Full Sangam', href: '/dashboard/game-config/FULL_SANGAM' },
      { label: 'Panel Chart', href: '/dashboard/game-numbers/panel-chart' },
    ],
  },

  // 11. Notice Management (Dropdown)
  {
    title: 'Notice Management',
    icon: 'file',
    items: [
      { label: 'Notice Management', href: '/dashboard/content/scrolling' },
      { label: 'Send Notification', href: '/dashboard/content/banners' },
    ],
  },

  // 12. Users Query (Direct link)
  { title: null, icon: 'support', items: [{ label: 'Users Query', href: '/dashboard/support/queries' }] },

  // 13. Settings (Dropdown)
  {
    title: 'Settings',
    icon: 'cog',
    items: [
      { label: 'Main Settings', href: '/dashboard/system/settings' },
      { label: 'Contact Settings', href: '/dashboard/support/contact' },
      { label: 'Clear Data', href: '/dashboard/system/audit-logs' },
      { label: 'Slider Images', href: '/dashboard/content/banners' },
      { label: 'QR Code Images', href: '/dashboard/wallet-activity/payment-settings' },
      { label: 'How To Play', href: '/dashboard/content/educational' },
      { label: 'Admin Users', href: '/dashboard/system/admin-users', permission: 'admins.manage' },
      { label: 'Roles & Permissions', href: '/dashboard/system/roles' },
    ],
  },
];
