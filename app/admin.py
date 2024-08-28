class StatsView(AdminBaseView):
    @expose('/', methods=['post', 'get'])
    def stats(self):
        global stats, from_date, to_date
        stats = dao.get_stats()
        from_date = to_date = None

        if request.method == 'POST':
            from_date = request.form.get('from-date')
            to_date = request.form.get('to-date')

            if not to_date:
                to_date = utils.format_date(datetime.now())

            stats = dao.get_stats(from_date, to_date)

        total_turn = 0
        total_sale = 0
        for s in stats:
            total_turn += s[2]
            total_sale += s[3]
        return self.render('/admin/stats.html', stats=stats, total_turn=total_turn,
                           total_sale=total_sale, empty=stats == [],
                           from_date=from_date, to_date=to_date)