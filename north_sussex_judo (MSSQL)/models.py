class Athlete:
    def __init__(self, id, name, training_plan, current_weight, competition_weight_category):
      self.id = id
      self.name = name
      self.training_plan = training_plan
      self.current_weight = current_weight
      self.competition_weight_category = competition_weight_category

class TrainingPlan:
    def __init__(self, plan_name, weekly_fee):
        self.plan_name = plan_name
        self.weekly_fee = weekly_fee

class Competition:
    def __init__(self, id, competition_name, entry_fee, date):
        self.id = id
        self.competition_name = competition_name
        self.entry_fee = entry_fee
        self.date = date

class ReportData:
  def __init__(self, name, weekly_fee, total_coaching_hours, competition_count, entry_fee, current_weight, competition_weight_category, limit):
      self.name = name
      self.weekly_fee = weekly_fee
      self.total_coaching_hours = total_coaching_hours
      self.competition_count = competition_count
      self.entry_fee = entry_fee
      self.current_weight = current_weight
      self.competition_weight_category = competition_weight_category
      self.limit = limit